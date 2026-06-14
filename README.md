# 🔍 Agentic RAG System — LangGraph-Powered Retrieval & Search

> A production-style Agentic RAG platform combining LangGraph orchestration, LangChain-compatible retrieval, pgvector semantic search, local LLM inference with Ollama, and Tavily-powered web search — delivering intelligent, grounded answers across documents, general knowledge, and real-time information.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-FF6B6B?style=flat)
![LangChain](https://img.shields.io/badge/LangChain-Retrieval-1C3C3C?style=flat)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20%7C%20llama3.2-black?style=flat)
![Tavily](https://img.shields.io/badge/Search-Tavily-blue?style=flat)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Overview

Most LLMs generate answers from their training data alone — leading to hallucinations and outdated responses. Standard RAG systems improve this by retrieving documents, but still force every query through the same retrieval pipeline regardless of whether retrieval is actually needed.

This system solves both problems by combining RAG, agent orchestration, and web search into a single intelligent query platform.

Instead of sending every question through the same retrieval pipeline, a **LangGraph agent** first determines the best strategy:

1. Route document-related questions to the **RAG pipeline**
2. Route general knowledge questions directly to the **LLM**
3. Route current-events or real-time questions to a **web search tool**

This architecture mirrors modern AI assistants that dynamically choose tools based on user intent rather than relying on retrieval alone.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI (async, Python) |
| **Agent Orchestration** | LangGraph |
| **Retrieval Framework** | LangChain |
| **Embeddings** | SentenceTransformers — `all-MiniLM-L6-v2` |
| **Vector Database** | PostgreSQL + `pgvector` extension |
| **LLM** | Ollama — `llama3.2` (runs locally) |
| **Web Search** | Tavily Search API |
| **ORM** | SQLAlchemy |
| **Containerization** | Docker |
| **Environment** | WSL (Ubuntu) on Windows |

---

## Features

### Agentic Query Routing
- LangGraph agent classifies each query and selects the optimal execution path
- LLM-powered query classification with multi-tool execution workflow
- Unified response interface across all tool types

### RAG Pipeline
- Document ingestion supporting `.txt` and `.pdf` files
- Text preprocessing — cleaning, normalization, and smart chunking
- Embedding generation via SentenceTransformers (`all-MiniLM-L6-v2`)
- Vector storage in PostgreSQL via `pgvector`
- LangChain-compatible retrieval abstraction over pgvector
- Cosine similarity search with HNSW indexing
- Source attribution with per-chunk similarity scoring

### Direct LLM Answering
- General knowledge and reasoning questions bypass retrieval entirely
- Reduces unnecessary latency for questions that don't require document context

### Web Search Integration
- Tavily-powered real-time web search for current events and live information
- Search results injected into prompt context for grounded web-sourced answers

### Observability
- Request-level latency tracking across retrieval, generation, and web search phases
- Latency debugging across all pipeline stages

---

## System Architecture

```
                         User Query
                              │
                              ▼
                    LangGraph Agent Router
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
     RAG Tool           Direct LLM Tool      Web Search Tool
         │                    │                    │
         ▼                    ▼                    ▼
 LangChain Retriever      Ollama LLM        Tavily Search
         │                                        │
         ▼                                        ▼
 PostgreSQL + pgvector                    Search Results
         │                                        │
         └────────────────────┬───────────────────┘
                              ▼
                    Prompt Construction
                              │
                              ▼
                    Ollama LLM Generation
                              │
                              ▼
              Grounded Answer + Source Citations
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

## Agent Workflow

### Query Classification

The system uses an LLM-based classifier to determine the best execution path for each request.

| Route | Trigger | Tool |
|---|---|---|
| **RAG** | Questions about uploaded documents | LangChain Retriever → pgvector |
| **Direct LLM** | General reasoning or knowledge questions | Ollama llama3.2 |
| **Web Search** | Current events, recent developments, live information | Tavily Search API |

The selected tool executes independently and returns results through a unified response interface.

---

## Project Structure

```
rag-ai-system/
│
├── app/
│   ├── main.py                          # FastAPI app entry point
│   ├── api/
│   │   └── routes/
│   │       ├── ingest.py                # Document ingestion endpoint
│   │       └── query.py                 # Agentic RAG query endpoint
│   ├── core/
│   │   ├── config.py                    # Environment and app settings
│   │   └── logging.py                   # Request logging and latency tracking
│   ├── db/
│   │   ├── session.py                   # SQLAlchemy database session
│   │   └── models.py                    # ORM models (document chunks, vectors)
│   ├── schemas/
│   │   ├── ingest.py                    # Pydantic request/response schemas
│   │   └── query.py
│   └── services/
│       ├── ingestion.py                 # Document loading, cleaning, chunking
│       ├── embedding.py                 # Embedding generation logic
│       ├── retrieval.py                 # Vector similarity search
│       ├── langchain_retriever_service.py  # LangChain retrieval abstraction
│       ├── direct_llm_service.py        # Direct LLM answering
│       ├── web_search_service.py        # Tavily web search integration
│       ├── llm_service.py               # Ollama LLM inference
│       ├── prompt_service.py            # Prompt construction logic
│       └── langgraph_agent_service.py   # LangGraph agent orchestration
│
├── scripts/
│   ├── init_db.py                       # Initialize pgvector schema
│   └── test_pipeline.py                 # End-to-end pipeline smoke test
│
├── sample_data/                         # Example documents for testing
├── uploaded_files/                      # Runtime document storage
├── requirements.txt
├── docker-compose.yml                   # PostgreSQL + pgvector container
├── .env.example                         # Environment variable template
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Docker Desktop (with WSL2 integration enabled)
- [Ollama](https://ollama.com) installed on Windows
- [Tavily API Key](https://tavily.com) (free tier available)
- WSL (Ubuntu)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Bteja272/rag-ai-system.git
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
# Edit .env with your settings
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
TAVILY_API_KEY=your_tavily_api_key_here
```

### Step 5 — Start PostgreSQL with pgvector

```bash
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

> **Note for WSL users:** Ollama runs on your Windows host. The API is accessible from WSL at `http://host.docker.internal:11434`.

### Step 8 — Start the API Server

```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

---

## API Reference

### `POST /ingest`

Upload and index a document into the vector store.

**Request:**
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

Submit a natural language query. The LangGraph agent automatically routes to the best tool.

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
  "route": "rag",
  "answer": "Retrieval-Augmented Generation (RAG) is an AI framework...",
  "sources": [
    {
      "chunk_id": "a3f2c1",
      "document": "intro_to_rag.pdf",
      "excerpt": "RAG combines the strengths of retrieval systems with generative models...",
      "similarity_score": 0.921
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
| No reranking | Similarity score alone determines chunk order; cross-encoder reranking would improve accuracy |
| No authentication | API endpoints are currently open — not suitable for public deployment as-is |
| No frontend | Query interaction is API-only |
| Single-document context | Retrieval pulls top-k chunks; very long answers may hit context window limits |
| Local LLM only | Ollama runs locally; no cloud LLM fallback currently implemented |

---

## Roadmap

- [ ] Hybrid search — BM25 + vector search for improved recall
- [ ] Cross-encoder reranking for improved retrieval relevance
- [ ] Multi-step reasoning workflows with LangGraph
- [ ] Conversation memory across query sessions
- [ ] Redis response caching for frequent queries
- [ ] Agent evaluation dashboard — faithfulness, relevance, context precision
- [ ] Multi-format ingestion — `.docx`, `.md`, web URLs
- [ ] Authentication — API key middleware
- [ ] Docker Compose full stack including API service

---

## Key Concepts

**Why agentic routing over fixed RAG?**
Fixed RAG pipelines retrieve documents for every query — even when retrieval adds no value. Agentic routing eliminates unnecessary retrieval latency for general knowledge questions and enables real-time answers via web search that a static RAG pipeline cannot provide.

**Why LangGraph over a simple if/else router?**
LangGraph models the agent as a stateful graph, enabling complex multi-step reasoning workflows, conditional branching, and future extensibility to parallel tool execution and conversation memory — none of which are possible with a simple conditional router.

**Why `all-MiniLM-L6-v2`?**
Compact, fast, and strong semantic similarity performance at 384 dimensions — well-suited for similarity search without excessive storage or compute cost.

**Why pgvector over Pinecone/Weaviate?**
pgvector co-locates the vector store with relational metadata in a single database, reducing infrastructure complexity. For production scale, managed vector databases offer better horizontal scaling, but pgvector is an excellent self-hosted choice.

**Why Ollama + llama3.2?**
Zero API costs, full data privacy, and no rate limits during development. Ollama makes local model serving simple and production-like.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

> Built as a production-style Agentic RAG platform demonstrating LangGraph orchestration, LangChain-compatible retrieval, pgvector semantic search, local LLM inference with Ollama, and Tavily-powered web search.