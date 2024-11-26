
# SQL Injection Scanner 💉

Este projeto é um scanner simples que verifica vulnerabilidades de SQL Injection em uma URL fornecida. Ele realiza um ataque básico de SQL Injection ao manipular os parâmetros da URL e os formulários na página, buscando sinais típicos de vulnerabilidades.

## Funcionalidades

- **Detecção de SQL Injection**: O scanner tenta injetar comandos SQL nos parâmetros de consulta da URL e nos parâmetros dos formulários.
- **Análise de Erros**: O scanner verifica a resposta da página para detectar mensagens de erro típicas de SQL Injection, como erros de sintaxe SQL ou mensagens de erro do banco de dados.
- **Suporte a Sessões e Cookies**: O scanner utiliza sessões HTTP e lida com cookies automaticamente, permitindo testar páginas que dependem de cookies para funcionalidades.

## Requisitos 📊

- Python 3.x
- Bibliotecas Python:
  - `requests`
  - `beautifulsoup4`

Você pode instalar as dependências utilizando o comando:

```bash
pip install requests beautifulsoup4
```

## Como Usar 📌

1. Clone o repositório ou baixe o código em seu computador.
2. Abra o terminal e execute o script passando a URL como argumento:

```bash
python3 sqli-scan.py <url>
```

Por exemplo: 

```bash
python3 sqli-scan.py "http://example.com?param1=value1&param2=value2"
```

3. O script irá fazer uma requisição para a URL fornecida, testar parâmetros de consulta (query parameters) e formulários na página em busca de vulnerabilidades SQL Injection.

## Funcionamento 🔗

1. **Fazendo a Requisição**:
   - O script faz uma requisição GET (ou POST, se necessário) para a URL fornecida. Ele trata cookies e cabeçalhos automaticamente, garantindo que a sessão seja preservada durante o processo.

2. **Analisando Parâmetros de Consulta**:
   - O script extrai os parâmetros da URL e tenta injetar payloads de SQL Injection comuns, como `' OR 1=1 --` ou `"' OR 'a' = 'a"`.

3. **Analisando Formulários**:
   - O script também escaneia os formulários na página e testa os parâmetros dos campos de entrada, procurando por vulnerabilidades em métodos POST.

4. **Verificando Vulnerabilidades**:
   - O script compara o HTML da resposta original com o HTML após a injeção do payload. Se houver uma diferença significativa, ou se erros típicos de SQL Injection forem encontrados, o script considera a página vulnerável.

## Exemplo de Saída

Caso o script encontre uma vulnerabilidade, você verá uma mensagem indicando a URL vulnerável:

```
Página carregada, iniciando o Scan...
Vulnerabilidade na URL: http://example.com?param1=' OR 1=1 --
```

Se não houver vulnerabilidade detectada, a saída será:

```
Página carregada, iniciando o Scan...
Não é Vulnerável
```

## Dicas

- **URLs Dinâmicas**: Certifique-se de testar URLs com parâmetros dinâmicos, como `id=1` ou `search=keyword`. ( Exemplo http://www.examplou.com/cat.php?id=1
- **Formulários**: O script também testa parâmetros em formulários HTML. Se um site tiver formulários, o script irá automaticamente tentar injetar payloads nos campos de entrada.
- **Testes em Ambientes Controlados**: Use este script apenas em ambientes de teste ou sites onde você tenha permissão para realizar testes de segurança. Realizar ataques de SQL Injection em sites sem permissão é ilegal.
- **Evoluindo o Script**: Este script pode ser melhorado adicionando mais tipos de payloads e técnicas de injeção, como técnicas de **Blind SQL Injection** ou **Error-Based SQL Injection**.

## Contribuindo

Se você deseja contribuir para o projeto, fique à vontade para abrir um **pull request** ou sugerir melhorias através de **issues**.
