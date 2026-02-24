import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Page Configuration & Custom Styling
st.set_page_config(page_title="QueryNest AI", layout="wide")

# This CSS forces a white background and cleans up the chat interface
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
    }
    .block-container {
        padding-top: 1.5rem;
    }
    /* Style the chat messages for better visibility on white */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key="Use your own key")

# ===============================
# LOAD EMBEDDINGS
# ===============================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embed_model = load_model()

# ===============================
# UTILITIES
# ===============================
def split_text(text, chunk_size=700, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_documents(files):
    full_text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    chunks = split_text(full_text)
    embeddings = embed_model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index, chunks

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "index" not in st.session_state:
    st.session_state.index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "last_score" not in st.session_state:
    st.session_state.last_score = None

# ===============================
# SIDEBAR (UPLOAD & SCORING)
# ===============================
with st.sidebar:
    st.header("📂 Documents")
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files and st.session_state.index is None:
        with st.spinner("Processing..."):
            index, chunks = process_documents(uploaded_files)
            st.session_state.index = index
            st.session_state.chunks = chunks
        st.success("Documents Ready")

    if st.button("Clear Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # --- SCORING SECTION ---
    st.divider()
    st.subheader("📊 Retrieval Metrics")
    if st.session_state.last_score is not None:
        # Converting L2 distance to a pseudo-confidence score
        # L2 distance of 0 is a perfect match.
        score = st.session_state.last_score
        st.metric(label="Retrieval Distance (L2)", value=f"{score:.4f}")
        st.caption("Lower is better (0.0 = exact match)")
    else:
        st.info("Ask a question to see retrieval score.")

# ===============================
# MAIN CHAT AREA
# ===============================
st.title("📄 QueryNest AI")
st.caption("AI Document Intelligence")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about your documents...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if st.session_state.index is None:
            reply = "Please upload documents first."
            st.markdown(reply)
        else:
            # RAG Retrieval
            query_embedding = embed_model.encode([user_input])
            distances, indices = st.session_state.index.search(
                np.array(query_embedding).astype('float32'), k=3
            )

            # Store the best distance (index 0) in session state for the sidebar
            st.session_state.last_score = float(distances[0][0])

            retrieved_chunks = [st.session_state.chunks[i] for i in indices[0]]
            context = "\n\n".join(retrieved_chunks)

            prompt = f"Answer strictly from context. If not found say: Information not found.\n\nContext:\n{context}\n\nQuestion:\n{user_input}"

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            reply = response.choices[0].message.content
            st.markdown(reply)
            
            # Save assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Rerun to update the sidebar score immediately
            st.rerun()