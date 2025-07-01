import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub  # using HF LLM instead of OpenAI

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    print(f"Looking for PDF at: {pdf_path}")
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    print(f"Extracted text length: {len(full_text)}")
    return full_text

# Step 2: Split text into chunks
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=100):
    print("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    print(f"Number of chunks: {len(chunks)}")
    return chunks

# Step 3: Create vector store from chunks
def create_vector_store(chunks):
    print("Creating vector store using Hugging Face embeddings...")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore

# Step 4: Build QA system using Hugging Face LLM
def build_qa_system(vectorstore):
    print("Setting up RetrievalQA with HuggingFace LLM...")

    # Use Hugging Face hosted model (like flan-t5 or any other supported one)
    llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 512})

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
    )
    return qa

# Step 5: Chat with the bot
def ask_questions(qa):
    print("\nYou can now ask questions about the syllabus.")
    print("Type 'exit' to stop.")
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            print("Exiting chatbot.")
            break
        response = qa.run(query)
        print(f"\nChatbot: {response}")

# Main function
def main():
    load_dotenv()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    syllabus_path = os.path.join(BASE_DIR, "doc", "4thsem_syllabus.pdf")

    # Step 1
    text = extract_text_from_pdf(syllabus_path)
    if not text.strip():
        print("❌ No text found in PDF. Please check the file.")
        return

    # Step 2
    chunks = split_text_into_chunks(text)

    # Step 3
    vectorstore = create_vector_store(chunks)

    # Step 4
    qa = build_qa_system(vectorstore)

    # Step 5
    ask_questions(qa)

if __name__ == "__main__":
    main()
