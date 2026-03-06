from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings

from .pdf_utils import load_and_split_pdf

vector_store = None
chat_history = []


def process_pdf(file_path):

    global vector_store

    docs = load_and_split_pdf(file_path)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(docs, embeddings)


def query_paper(question):

    global vector_store
    global chat_history

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in docs])

    llm = Ollama(model="llama3")

    prompt = f"""
You are a research assistant.

Answer the question based on the context below.

Context:
{context}

Previous conversation:
{chat_history}

Question:
{question}

Answer:
"""

    answer = llm.invoke(prompt)

    chat_history.append((question, answer))

    return answer