import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

UPLOAD_DIR = "./uploaded_pdfs"
PERSIST_DIR = "./chroma_store"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)

# Embedding model (downloaded once, cached locally)
EMBEDDING_MODEL = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


def load_vectorstore(uploaded_files):
    """
    Save uploaded PDF files, chunk them, embed them,
    and store in a persistent ChromaDB vectorstore.
    """
    file_paths = []

    # Save uploaded files to disk
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    all_chunks = []

    for file_path in file_paths:
        print(f"📄 Loading: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        all_chunks.extend(chunks)
        print(f"   ✅ {len(chunks)} chunks created from {Path(file_path).name}")

    if not all_chunks:
        raise ValueError("No content could be extracted from the uploaded PDFs.")

    print(f"🔍 Embedding {len(all_chunks)} total chunks...")

    # Load existing vectorstore or create new
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=EMBEDDING_MODEL,
        persist_directory=PERSIST_DIR
    )

    print("✅ Vectorstore updated successfully.")
    return vectorstore


def get_vectorstore():
    """
    Load the existing ChromaDB vectorstore from disk.
    """
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=EMBEDDING_MODEL
    )
