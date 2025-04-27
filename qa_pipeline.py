import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load PDF
def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Split Text
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return chunks

# Embed Text
def embed_text(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # small & fast
    embeddings = model.encode(chunks)
    return embeddings

# Build Vector Store
def build_vector_store(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

# Search
def search_index(query, chunks, index, model, top_k=5):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k)
    results = [chunks[i] for i in I[0]]
    return results
