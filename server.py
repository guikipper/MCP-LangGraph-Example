from mcp.server.fastmcp import FastMCP # Simplifica a criação de servidores MCP
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from ingest import load_bellavista_documents

from dotenv import load_dotenv
import os

#Google
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CREDENTIALS_FILE = "credentials.json"  
# Escopo de permissão para acessar o Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# Função para autenticar e obter serviço do Google Drive
def authenticate_drive():
    creds = None
    if os.path.exists("token.json"):  
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid: 
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return build("drive", "v3", credentials=creds)

# Criar serviço autenticado do Google Drive
drive_service = authenticate_drive()

vectorstore = load_bellavista_documents()
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

mcp = FastMCP("TesteServer", host="127.0.0.1", port="3000")

#pip install langchain langchain-openai langchain-core langchain-chroma chromadb

def get_drive_service():
    creds = Credentials.from_authorized_user_file("token.json")
    return build("drive", "v3", credentials=creds)

@mcp.tool(description="Lista os arquivos do Google Drive.")
def list_drive_files() -> list[str]:
    service = get_drive_service()
    results = service.files().list(fields="files(id, name)").execute()
    files = results.get("files", [])
    return [file["name"] for file in files]

@mcp.tool(description="Busca arquivos no Google Drive pelo nome.")
def search_drive_files(query: str) -> list[str]:
    service = get_drive_service()
    results = service.files().list(q=f"name contains '{query}'", fields="files(id, name)").execute()
    files = results.get("files", [])
    return [file["name"] for file in files]

@mcp.tool()
def add(a: int, b:int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b:int) -> int:
    return a * b

@mcp.tool(description="Tool usada para obter dados do Chroma.")
def search_docs(query: str) -> str:
    results = retriever.invoke(query)
    texts = []
    for i, doc in enumerate(results):
        texts.append(f"Document {i + 1}:\n{doc.page_content}")
    return "\n\n".join(texts)

@mcp.resource("resource://hello", description="Uma saudação de Hello!")
def resource_hello() -> str:
    return "Hello from the resource endpoint!"

@mcp.resource("resouce://food/{item}")
def resouce_food(item: str) -> str:
    if item.lower() == "pizza":
        return "Bella Vista's wood-fired pizza is priced at 10$"
    return "No details available for that item."

@mcp.prompt(name="friendly_greeting", description="Generate a short greeting message")
def prompt_friendly_greeting(name: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": {"type": "text", "text": "You are a friendly helper"}
        },
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"Welcome, {name}! How can I assist you today?",
            },
        },
    ]

if __name__ == "__main__":
    mcp.run(transport="sse")