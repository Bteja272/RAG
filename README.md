# 🔍 RAG AI System — Retrieval-Augmented Generation

> A production-style AI system that lets users query document collections and receive accurate, grounded answers powered by local LLMs — with full source attribution.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20%7C%20llama3.2-black?style=flat)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Overview

Most LLMs generate answers from their training data alone — which leads to hallucinations and outdated responses. This system solves that by combining **semantic retrieval** with **local LLM generation**:

1. Documents are ingested, chunked, and converted into vector embeddings
2. When a user submits a query, the system retrieves the most semantically relevant chunks
3. Those chunks are injected into a prompt sent to a local LLM
4. The model generates a grounded answer, citing the exact source documents

This architecture mirrors what production AI platforms like Perplexity, Notion AI, and enterprise search tools use at scale.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI (async, Python) |
| **Embeddings** | SentenceTransformers — `all-MiniLM-L6-v2` |
| **Vector Database** | PostgreSQL + `pgvector` extension |
| **LLM** | Ollama — `llama3.2` (runs locally) |
| **ORM** | SQLAlchemy |
| **Containerization** | Docker |
| **Environment** | WSL (Ubuntu) on Windows |

---

## Features

- **Document ingestion** — supports `.txt` and `.pdf` files
- **Text preprocessing** — cleaning, normalization, and smart chunking
- **Embedding generation** — converts document chunks into dense vector representations
- **Vector storage** — persists embeddings in PostgreSQL via `pgvector`
- **Semantic search** — cosine similarity retrieval over stored vectors
- **Grounded generation** — local LLM answers are anchored to retrieved document content
- **Source attribution** — every response includes the originating document chunks
- **Latency tracking** — request-level logging for retrieval and generation times
- **REST API** — clean FastAPI endpoints for ingestion and querying

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER QUERY                           │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Query Embedding    │  ← SentenceTransformers
                  │  (all-MiniLM-L6-v2) │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  pgvector Search    │  ← Cosine Similarity
                  │  (PostgreSQL)       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Top-k Chunks       │  ← Retrieved Context
                  │  + Source Metadata  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Prompt Builder     │  ← Context Injection
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Ollama LLM         │  ← llama3.2 (local)
                  │  Generation         │
                  └──────────┬──────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              GROUNDED ANSWER + SOURCE CITATIONS             │
└─────────────────────────────────────────────────────────────┘
```

### Document Ingestion Flow

```
Raw Document (PDF / TXT)
        │
        ▼
   Text Extraction
        │
        ▼
   Cleaning & Normalization
        │
        ▼
   Chunking (fixed-size with overlap)
        │
        ▼
   Embedding Generation (SentenceTransformers)
        │
        ▼
   Vector Storage (PostgreSQL + pgvector)
```

---

## Project Structure

```
rag-ai-system/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   └── routes/
│   │       ├── ingest.py        # Document ingestion endpoint
│   │       └── query.py         # RAG query endpoint
│   ├── core/
│   │   ├── config.py            # Environment and app settings
│   │   └── logging.py           # Request logging and latency tracking
│   ├── db/
│   │   ├── session.py           # SQLAlchemy database session
│   │   └── models.py            # ORM models (document chunks, vectors)
│   ├── schemas/
│   │   ├── ingest.py            # Pydantic request/response schemas
│   │   └── query.py
│   └── services/
│       ├── ingestion.py         # Document loading, cleaning, chunking
│       ├── embedding.py         # Embedding generation logic
│       ├── retrieval.py         # Vector similarity search
│       └── generation.py        # Prompt construction + Ollama LLM call
│
├── scripts/
│   ├── init_db.py               # Initialize pgvector schema
│   └── test_pipeline.py         # End-to-end pipeline smoke test
│
├── sample_data/                 # Example documents for testing
├── uploaded_files/              # Runtime document storage
├── requirements.txt
├── docker-compose.yml           # PostgreSQL + pgvector container
├── .env.example                 # Environment variable template
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Docker Desktop (with WSL2 integration enabled)
- [Ollama](https://ollama.com) installed on Windows
- WSL (Ubuntu)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/rag-ai-system.git
cd rag-ai-system
```

### Step 2 — Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your database URL and settings
```

Example `.env`:
```env
DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb
OLLAMA_BASE_URL=http://host.docker.internal:11434
EMBED_MODEL=all-MiniLM-L6-v2
OLLAMA_MODEL=llama3.2
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K_RESULTS=5
```

### Step 5 — Start PostgreSQL with pgvector

```bash
docker start rag-postgres
# Or, if starting fresh:
docker-compose up -d
```

### Step 6 — Initialize the Database Schema

```bash
python scripts/init_db.py
```

### Step 7 — Start the Ollama Model (Windows Host)

```bash
ollama run llama3.2
```

> **Note for WSL users:** Ollama runs on your Windows host. The API is accessible from WSL at `http://host.docker.internal:11434`. Ensure Ollama is running before starting the API.

### Step 8 — Start the API Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## API Reference

### `POST /ingest`

Upload and index a document into the vector store.

**Request** (multipart form):

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@sample_data/intro_to_rag.pdf"
```

**Response:**

```json
{
  "status": "success",
  "filename": "intro_to_rag.pdf",
  "chunks_indexed": 42,
  "latency_ms": 1840
}
```

---

### `POST /query`

Submit a natural language query and receive a grounded answer.

**Request:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Retrieval-Augmented Generation?"}'
```

**Response:**

```json
{
  "query": "What is Retrieval-Augmented Generation?",
  "answer": "Retrieval-Augmented Generation (RAG) is an AI framework that enhances large language model responses by retrieving relevant documents from an external knowledge base before generating an answer. Instead of relying solely on parameters learned during training, the model grounds its response in retrieved context, reducing hallucinations and enabling up-to-date answers.",
  "sources": [
    {
      "chunk_id": "a3f2c1",
      "document": "intro_to_rag.pdf",
      "excerpt": "RAG combines the strengths of retrieval systems with generative models...",
      "similarity_score": 0.921
    },
    {
      "chunk_id": "b7d4e9",
      "document": "llm_survey.txt",
      "excerpt": "Retrieval-augmented approaches significantly reduce factual hallucination rates...",
      "similarity_score": 0.887
    }
  ],
  "retrieval_latency_ms": 38,
  "generation_latency_ms": 1420,
  "total_latency_ms": 1458
}
```

---

## Known Limitations

| Limitation | Notes |
|---|---|
| Retrieval noise | Small document sets can return low-relevance chunks — improves with larger corpora |
| No reranking | Similarity score alone determines chunk order; cross-encoder reranking would improve accuracy |
| No authentication | API endpoints are currently open — not suitable for public deployment as-is |
| No frontend | Query interaction is API-only; UI planned (see roadmap) |
| Single-document context | Retrieval pulls top-k chunks; very long answers may hit context window limits |

---

## Roadmap

- [ ] **Hybrid search** — combine dense vector search with BM25 keyword search for better recall
- [ ] **Cross-encoder reranking** — rerank retrieved chunks for improved answer relevance
- [ ] **Redis caching** — cache frequent queries to reduce latency and LLM calls
- [ ] **Evaluation metrics dashboard** — faithfulness, answer relevance, and context precision scoring
- [ ] **Streamlit frontend** — interactive UI for document upload and querying
- [ ] **Multi-format ingestion** — add support for `.docx`, `.md`, and web URLs
- [ ] **Authentication** — API key middleware for endpoint protection
- [ ] **Docker Compose full stack** — containerize the entire system including the API service

---

## Key Concepts

**Why RAG instead of fine-tuning?**  
Fine-tuning embeds knowledge into model weights — it's expensive, slow to update, and prone to catastrophic forgetting. RAG keeps knowledge in an external store that can be updated in real time without retraining the model.

**Why `all-MiniLM-L6-v2`?**  
It's a compact, fast embedding model that delivers strong semantic similarity performance. At 384 dimensions, it's well-suited for similarity search without excessive storage or compute cost.

**Why pgvector over Pinecone/Weaviate?**  
pgvector keeps the vector store co-located with relational metadata in a single database, reducing infrastructure complexity. For production scale, managed vector databases offer better horizontal scaling, but pgvector is an excellent choice for a self-hosted system.

**Why Ollama + llama3.2?**  
Running the LLM locally means zero API costs, full data privacy, and no rate limits during development. Ollama makes local model serving simple and production-like.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed change.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

> Built as a production-style ML portfolio project demonstrating RAG pipeline design, vector search, and local LLM integration.