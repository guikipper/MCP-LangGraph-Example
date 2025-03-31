# 📌 MCP LangGraph Example

Este repositório contém um exemplo de integração entre MCP e LangGraph, utilizando LangChain e OpenAI.

## 📥 Clonando o projeto e instalando dependências

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/mcp-langgraph-example.git
   cd mcp-langgraph-example
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv .venv
   ```

3. Ative o ambiente virtual:
   - **Windows:**
     ```sh
     .venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```sh
     source .venv/bin/activate
     ```

4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## 📄 Configuração das Credenciais do Google Drive

Para o correto funcionamento do projeto, é necessário obter um arquivo de credenciais do Google Drive e colocá-lo na raiz do projeto com o nome:

```
credentials.json
```

## 🔑 Configuração do OpenAI

Crie um arquivo `.env` na raiz do projeto e adicione a chave da OpenAI:

```
OPENAI_API_KEY=sua-chave-aqui
```

## 🚀 Rodando o servidor

Com tudo configurado, inicie o servidor executando:

```sh
python server.py
```

Durante a execução, é necessário fazer login e autenticar com o Google.

## 🛠 Testando o agente

Com o servidor rodando, você pode testar enviando requisições via `host_and_client.py`:

```sh
python host_and_client.py
```

Teste à vontade com os prompts para mandar novas requisições ao agente! 😃

## ⚠️ Possíveis Problemas na Instalação

Caso o `requirements.txt` não instale corretamente as dependências, tente instalar manualmente com:

```sh
pip install langchain-mcp-adapters langgraph langchain-openai
```

Se precisar de ajuda, só entrar em contato! 🚀
