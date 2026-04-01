# 🤖 RAG Chatbot 2.0

A full-stack AI chatbot that lets you upload PDF documents and ask questions about them using Retrieval-Augmented Generation (RAG). Built with FastAPI, Pinecone, Google Gemini, and Streamlit.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [API Keys Setup](#api-keys-setup)
- [Running the Project](#running-the-project)
- [How to Use](#how-to-use)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## Overview

RAG Chatbot 2.0 allows users to upload one or more PDF files and ask natural language questions about their contents. The backend embeds the document text into a Pinecone vector database using Google's embedding model, and answers questions using Google Gemini (LLM) with retrieved context — making responses grounded in your actual documents.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | Google `embedding-001` (768 dims) |
| Vector Store | Pinecone (Serverless) |
| PDF Parsing | PyPDF |
| Orchestration | LangChain |

---

## Project Structure

```
rag_chatbot/
├── client/                        # Streamlit frontend
│   ├── components/
│   │   ├── upload.py              # PDF upload UI component
│   │   └── history_download.py    # Chat history download component
│   ├── utils/
│   │   ├── __init__.py
│   │   └── api.py                 # API calls to backend
│   ├── app.py                     # Main Streamlit app
│   ├── config.py                  # Frontend config (API base URL)
│   └── requirements.txt
│
└── server/                        # FastAPI backend
    ├── modules/
    │   ├── __init__.py
    │   ├── load_vectorstore.py    # PDF processing + Pinecone upsert
    │   ├── llm.py                 # LLM chain setup (Gemini)
    │   └── query_handlers.py      # Query processing + response formatting
    ├── main.py                    # FastAPI app + routes
    ├── logger.py                  # Logging config
    ├── .env                       # API keys (not committed to git)
    ├── .env.example               # Template for .env
    └── requirements.txt
```

---

## Prerequisites

- **Python 3.11** (recommended — Python 3.12+ may cause compatibility issues with LangChain)
- A **Pinecone** account → https://app.pinecone.io
- A **Google AI Studio** API key → https://aistudio.google.com/app/apikey

---

## Setup & Installation

### 1. Clone or extract the project

```bash
cd rag_chatbot
```

### 2. Set up backend virtual environment

```powershell
cd server
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up frontend virtual environment

Open a second terminal:

```powershell
cd client
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## API Keys Setup

### Pinecone
1. Go to https://app.pinecone.io
2. Create a new index with these settings:
   - **Name:** `ragbot` (or any name you prefer)
   - **Dimensions:** `768`
   - **Metric:** `cosine`
   - **Type:** Serverless (AWS, us-east-1)
3. Go to **API Keys** in the sidebar and copy your key

### Google AI Studio
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key

### Configure .env

Inside the `server/` folder, rename `.env.example` to `.env` and fill in:

```env
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=ragbot
```

---

## Running the Project

You need **two terminals open at the same time.**

**Terminal 1 — Backend:**
```powershell
cd server
venv\Scripts\activate
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

**Terminal 2 — Frontend:**
```powershell
cd client
venv\Scripts\activate
streamlit run app.py
```

Frontend opens at: `http://localhost:8501`

---

## How to Use

1. Open `http://localhost:8501` in your browser
2. Confirm you see **"🟢 Backend is running"**
3. Upload one or more PDF files using the sidebar
4. Click **"Process PDFs"** — this embeds them into Pinecone
5. Type your question in the chat box and press Enter
6. The bot answers based on your uploaded documents
7. Expand **"📚 Sources"** under any answer to see which parts of your PDFs were used
8. Download your chat history as TXT or JSON from the sidebar

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/test` | Health check |
| `POST` | `/upload_pdfs/` | Upload and embed PDF files |
| `POST` | `/ask/` | Ask a question, get an answer |

Full interactive API docs available at: `http://127.0.0.1:8000/docs`

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'langchain.chains'`**
→ Run: `pip install --upgrade langchain langchain-community langchain-core`

**`Exception: pinecone-client has been renamed to pinecone`**
→ Run: `pip uninstall pinecone-client -y && pip install pinecone`

**`Pydantic V1 not compatible with Python 3.14`**
→ Recreate your venv using Python 3.11: `py -3.11 -m venv venv`

**`Backend is not running` on the frontend**
→ Make sure Terminal 1 (backend) is running without errors before opening the frontend

**`.env` keys not loading**
→ Ensure your `.env` file is inside the `server/` folder, not the root

---

## Author

**Ishaan Sensharma**  
B.Tech CSE (AI/ML) — NIIT University  
GitHub: [IshaanSensharma-official](https://github.com/IshaanSensharma-official)
