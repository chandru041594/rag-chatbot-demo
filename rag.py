from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

llm = ChatOllama(model="llama3.2", temperature=0)

def ask_question(question: str) -> tuple[str, list[int]]:
    docs = retriever.invoke(question)
    if not docs:
        return "I couldn't find that information in the PDF.", []

    context = "\n\n".join(
        f"[Page {doc.metadata.get('page', 0) + 1}] {doc.page_content}"
        for doc in docs
    )

    response = llm.invoke(
        "Answer only from the PDF context. If the answer isn't there, say so. "
        "Cite page numbers.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )

    pages = sorted({
        doc.metadata["page"] + 1
        for doc in docs
        if "page" in doc.metadata
    })
    return response.content, pages