# 🦉 QueryNest AI

**Precision Document Intelligence & Semantic Retrieval System**

QueryNest AI is a high-performance **Retrieval-Augmented Generation (RAG)** platform designed to transform static PDF documents into interactive, queryable knowledge bases. Unlike standard chatbots, QueryNest AI focuses on **mathematical grounding** by providing real-time retrieval metrics to ensure every answer is backed by your data.

---

## 🚀 Features

* **Lightning-Fast Inference:** Powered by **Groq LPU™** technology using the `llama-3.1-8b-instant` model for near-instant responses.
* **Semantic Vector Search:** Utilizes **FAISS** (Facebook AI Similarity Search) for efficient similarity matching.
* **Observability:** Integrated **Retrieval Distance (L2)** scoring in the sidebar to monitor how closely the source text matches your query.
* **Clean UI:** A minimalist, professional interface built with **Streamlit**, featuring a white-themed chat area and structured sidebar.

---

## 🛠️ Technical Stack

* **LLM:** Llama 3.1 (via Groq Cloud API)
* **Orchestration:** Python & Streamlit
* **Vector Store:** FAISS (IndexFlatL2)
* **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers)
* **PDF Processing:** PyPDF2

---

## ⚙️ How it Works (The Pipeline)

1. **Ingestion:** User uploads one or multiple PDF documents.
2. **Chunking:** The system extracts text and splits it into optimized chunks (700 characters) with a 150-character overlap to preserve context.
3. **Embedding:** Text chunks are converted into vector representations using the `all-MiniLM-L6-v2` model.
4. **Retrieval:** When a question is asked, the system embeds the query and searches the **FAISS** index for the top 3 most relevant segments using Euclidean (L2) distance.
5. **Grounded Response:** The LLM generates a response strictly based on the retrieved context. If the information isn't there, it won't hallucinate.

---

## 📊 Understanding the Scores

QueryNest AI provides transparency through its **Retrieval Distance (L2)** metric:

* **Score < 1.0:** **High Confidence** — Direct semantic match found. ✅
* **Score 1.0 – 1.5:** **Good Relevance** — Strong conceptual connection detected. 🔍
* **Score > 1.6:** **Low Confidence** — The context is loosely related; results should be verified. ⚠️

---
<img width="1914" height="859" alt="image" src="https://github.com/user-attachments/assets/0b447c15-0c49-4a02-8abd-c15b22f20d45" />



<img width="1917" height="866" alt="Screenshot 2026-02-24 154010" src="https://github.com/user-attachments/assets/3c45c074-d170-473d-9d1b-15c5e7298485" />


## 📥 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/QueryNest-AI.git
cd QueryNest-AI

```


2. **Install dependencies:**
```bash
pip install streamlit groq pypdf2 sentence-transformers faiss-cpu numpy

```


3. **Set up API Key:**
Replace `"Use your own key"` in the code with your actual [Groq API Key](https://console.groq.com/).
4. **Run the application:**
```bash
streamlit run app.py

```



---

## 🔬 Future Roadmap

* Support for multiple file formats (DOCX, TXT, CSV).
* Integration of **RAGAS** for automated evaluation of retrieval quality.
* Persistent vector storage for faster session re-loading.
