import streamlit as st
from qa_pipeline import load_pdf, split_text, embed_text, build_vector_store, search_index
from sentence_transformers import SentenceTransformer
import numpy as np

from llm_generator import generate_answer


# import sys
# import asyncio
# import os

# Fix for Windows and PyTorch conflict
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     st.set_option('server.fileWatcherType', 'none')

#     os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

st.title("📄 PDF Q&A Chatbot")


uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully!")

    text = load_pdf("temp.pdf")
    chunks = split_text(text)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embed_text(chunks)
    index = build_vector_store(np.array(embeddings))

    st.session_state.chunks = chunks
    st.session_state.index = index
    st.session_state.model = model

if "index" in st.session_state:
    query = st.text_input("Ask a question about the PDF:")
    if query:
        results = search_index(query, st.session_state.chunks, st.session_state.index, st.session_state.model)
        
        context = " ".join(results)[:2000]  # small limit, to fit into model input
        answer = generate_answer(context, query)

        st.write("### 📢 Answer:")
        st.write(answer)

