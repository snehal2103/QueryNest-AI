# 🦉 QueryNest AI

**Precision Document Intelligence via RAG & Groq**

QueryNest AI is a high-performance **Retrieval-Augmented Generation** platform that turns static PDFs into queryable knowledge bases. It prioritizes **mathematical grounding** by exposing retrieval metrics to the user.

---

### 🌟 Key Features

* **Lightning Speed:** Powered by **Groq LPU™** (`llama-3.1-8b-instant`) for near-instant answers.
* **Vector Search:** Uses **FAISS (IndexFlatL2)** for high-speed semantic retrieval.
* **Trust Metrics:** Real-time **L2 Distance** tracking to distinguish between a "fact" and a "hallucination."
* **Pro UI:** Minimalist **Streamlit** interface designed for document auditing.

---

### 🛠️ Technical Stack

* **LLM:** Llama 3.1
* **Embeddings:** `all-MiniLM-L6-v2`
* **Vector Store:** FAISS
* **PDF Engine:** PyPDF2
* **Frontend:** Streamlit

---

### ⚙️ How It Works

1. **Ingest:** PDF text is extracted and split into **700-character chunks**.
2. **Embed:** Chunks are vectorized using Sentence-Transformers.
3. **Retrieve:** Queries are compared against the index using **Euclidean Distance**.
4. **Respond:** The LLM generates a response **strictly grounded** in the retrieved context.

---

### 📊 Confidence Scoring (L2)

| Score | Confidence | Meaning |
| --- | --- | --- |
| **< 1.0** | **High** | Direct semantic match found ✅ |
| **1.0 - 1.5** | **Medium** | Strong conceptual connection 🔍 |
| **> 1.6** | **Low** | Likely out-of-context; verify manually ⚠️ |

---


<img width="1914" height="859" alt="Screenshot 2026-02-24 155108" src="https://github.com/user-attachments/assets/c95715c9-7487-4cf2-8b26-c43a0cdd07b7" />





<img width="1917" height="866" alt="Screenshot 2026-02-24 154010" src="https://github.com/user-attachments/assets/e92d8bdc-afe3-4c75-a063-dde8a8828352" />






### 🚀 Quick Start

```bash
# Clone & Install
git clone https://github.com/your-username/QueryNest-AI.git
pip install streamlit groq pypdf2 sentence-transformers faiss-cpu numpy

# Set your Groq API Key in app.py and run:
streamlit run app.py

```

---
