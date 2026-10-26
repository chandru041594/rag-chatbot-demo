from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

PDF_PATH = Path("data/LeavePolicy.pdf")

if not PDF_PATH.exists():
    raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

pages = PyPDFLoader(str(PDF_PATH)).load()

chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
).split_documents(pages)

Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="chroma_db",
)

print(f"Indexed {len(chunks)} chunks.")