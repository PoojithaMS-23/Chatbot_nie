# main.py

from PyPDF2 import PdfReader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

PDF_PATH = "Chatbot_nie/doc/4thsem_syllabus.pdf"
VECTOR_DB_DIR = "faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def extract_text_from_pdf(path):
    print(f"Looking for PDF at: {path}")
    reader = PdfReader(path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    print(f"Extracted text length: {len(text)}")
    return text

def split_text(text):
    print("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    print(f"Number of chunks: {len(chunks)}")
    return chunks

def create_vector_store(chunks):
    print("Creating vector store using Hugging Face embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    docs = [Document(page_content=chunk, metadata={"source": "4thsem_syllabus.pdf"}) for chunk in chunks]
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local(VECTOR_DB_DIR)
    print("Vector store created and saved.")
    return vectorstore

def load_vector_store():
    print("Loading existing vector store...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    return FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)

def chatbot_query(vectorstore, query):
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "Sorry, this question is out of scope."
    
    response = "\n\n".join([f"From {r.metadata['source']}:\n{r.page_content}" for r in results])
    return f"Based on the documents:\n\n{response}"

def main():
    if not os.path.exists(VECTOR_DB_DIR):
        text = extract_text_from_pdf(PDF_PATH)
        chunks = split_text(text)
        vectorstore = create_vector_store(chunks)
    else:
        vectorstore = load_vector_store()

    print("\n📘 Chatbot is ready. Type your question (or 'exit' to quit):")
    while True:
        query = input("\n🧠 You: ")
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting chatbot.")
            break
        response = chatbot_query(vectorstore, query)
        print(f"\n🤖 Bot: {response}")

if __name__ == "__main__":
    main()
