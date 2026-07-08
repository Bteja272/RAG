# 🔍 Agentic RAG System
### LangGraph-Powered Intelligent Query Routing

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-FF6B6B?style=flat)
![LangChain](https://img.shields.io/badge/LangChain-Retrieval-1C3C3C?style=flat)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20%7C%20llama3.2-black?style=flat)
![Tavily](https://img.shields.io/badge/Search-Tavily-blue?style=flat)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> Not every question needs document retrieval. Not every question can be answered from training data. This system knows the difference.

---

## The Routing Problem

Standard RAG systems send every query through the same retrieval pipeline — even when retrieval adds zero value. Ask "What is the capital of France?" and a fixed RAG system still searches your vector database, finds nothing relevant, and wastes 38ms before answering from LLM knowledge it already had.

Ask "What happened in AI news today?" and a fixed RAG system answers from stale training data because it has no web search capability.

This system routes intelligently:

| Query | Route | Why |
|---|---|---|
| "Summarize the uploaded research paper" | RAG pipeline | Document-specific, needs retrieval |
| "What is the capital of France?" | Direct LLM | General knowledge, no retrieval needed |
| "What happened in AI news this week?" | Tavily web search | Real-time, beyond training data |

**The result:** faster answers when retrieval isn't needed, grounded answers when it is, and live answers when neither is enough.

---

## What Makes This Different From a Basic RAG Tutorial

Most RAG implementations are fixed pipelines — query goes in, retrieved chunks come out, LLM generates. This is not that.

- **LangGraph state machine** not a simple if/else router — enables multi-step reasoning, conditional branching, and future parallel tool execution
- **Three-tool agentic system** with LLM-based query classification deciding the execution path at runtime
- **HNSW indexing** on pgvector not a flat cosine scan — sub-linear retrieval time at scale
- **Source attribution** with per-chunk similarity scoring — every answer cites the exact document chunks used
- **Latency tracked per pipeline phase** — retrieval, generation, and web search independently measured

---

## How It Works

```
User Query
     ↓
LangGraph Agent Router  ← LLM-based query classification
     │
     ├──────────────────────────────────┐──────────────────────┐
     ▼                                  ▼                      ▼
RAG Tool                         Direct LLM Tool        Web Search Tool
~38ms retrieval                  0ms retrieval           ~200ms search
+ ~1400ms generation             + ~1400ms generation    + ~1400ms generation
     │                                  │                      │
LangChain Retriever               Ollama llama3.2        Tavily Search API
     │                                                         │
PostgreSQL + pgvector                               Live search results
(HNSW cosine similarity)
     │                                  │                      │
     └──────────────────────────────────┴──────────────────────┘
                              ▼
                    Prompt Construction
                              ▼
                    Ollama LLM Generation
                              ▼
              Grounded Answer + Source Citations
```

---

## Document Ingestion Pipeline

```
PDF / TXT Upload
     ↓
Text Extraction
     ↓
Cleaning + Normalization
     ↓
Fixed-size chunking (512 tokens, 64 overlap)
     ↓
SentenceTransformers all-MiniLM-L6-v2 embeddings (384 dimensions)
     ↓
PostgreSQL + pgvector with HNSW index
```

Chunks scoring below **0.7 cosine similarity** are filtered from context before generation — reducing hallucination risk from low-relevance retrievals.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (async, Python) |
| Agent Orchestration | LangGraph |
| Retrieval Framework | LangChain |
| Embeddings | SentenceTransformers — `all-MiniLM-L6-v2` |
| Vector Database | PostgreSQL + `pgvector` (HNSW index) |
| LLM | Ollama — `llama3.2` (local inference) |
| Web Search | Tavily Search API |
| ORM | SQLAlchemy |
| Containerization | Docker |

---

## 🏗️ Key Technical Decisions

**Why LangGraph over a simple if/else router?**
A conditional router is a dead end — it handles three routes today and requires a rewrite to add a fourth. LangGraph models the agent as a stateful directed graph: adding a new tool is adding a new node and edge, not restructuring control flow. It also enables future multi-step reasoning where one tool's output informs the next tool's input — impossible with a router.

**Why agentic routing over fixed RAG?**
Fixed RAG retrieves documents for every query regardless of relevance. For general knowledge questions this wastes 38ms and potentially injects irrelevant context that degrades answer quality. For real-time questions it fails entirely. Agentic routing eliminates both failure modes.

**Why pgvector over Pinecone or Weaviate?**
pgvector co-locates the vector store with relational metadata — chunk text, document ID, source filename — in a single PostgreSQL database. No cross-service round trips for metadata lookups, no separate infrastructure to manage. For a self-hosted system the operational simplicity outweighs the horizontal scaling advantages of managed vector databases.

**Why HNSW indexing?**
HNSW (Hierarchical Navigable Small World) provides approximate nearest-neighbor search in sub-linear time — O(log n) versus O(n) for flat cosine scan. At small corpora the difference is negligible; at thousands of chunks it's the difference between 38ms and 380ms retrieval latency.

**Why Ollama + llama3.2 over OpenAI?**
Zero API costs, full data privacy, and no rate limits during development. The architecture supports swapping in any OpenAI-compatible endpoint — the LLM is a pluggable component, not a hard dependency.

**Why `all-MiniLM-L6-v2`?**
384-dimensional embeddings — compact enough for fast similarity search, expressive enough for strong semantic matching. Benchmark performance on semantic textual similarity tasks is comparable to models twice its size at a fraction of the inference cost.

---

## 🚀 Quick Start

```bash
# Clone and set up environment
git clone https://github.com/Bteja272/rag-ai-system.git
cd rag-ai-system
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your TAVILY_API_KEY to .env

# Start PostgreSQL + pgvector
docker-compose up -d
python scripts/init_db.py

# Start Ollama (Windows host)
ollama run llama3.2

# Start API
uvicorn app.main:app --reload
```

API at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

---

## 🔌 API Reference

### Ingest a document

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@sample_data/intro_to_rag.pdf"
```
```json
{
  "status": "success",
  "filename": "intro_to_rag.pdf",
  "chunks_indexed": 42,
  "latency_ms": 1840
}
```

### Query — agent routes automatically

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Retrieval-Augmented Generation?"}'
```
```json
{
  "query": "What is Retrieval-Augmented Generation?",
  "route": "rag",
  "answer": "Retrieval-Augmented Generation (RAG) is an AI framework...",
  "sources": [
    {
      "chunk_id": "a3f2c1",
      "document": "intro_to_rag.pdf",
      "excerpt": "RAG combines the strengths of retrieval systems...",
      "similarity_score": 0.921
    }
  ],
  "retrieval_latency_ms": 38,
  "generation_latency_ms": 1420,
  "total_latency_ms": 1458
}
```

The `route` field tells you which tool handled the query: `rag` · `direct_llm` · `web_search`

---

## 📁 Project Structure

```
rag-ai-system/
├── app/
│   ├── main.py
│   ├── api/routes/
│   │   ├── ingest.py                    Document ingestion endpoint
│   │   └── query.py                     Agentic RAG query endpoint
│   ├── core/
│   │   ├── config.py                    Environment settings
│   │   └── logging.py                   Per-phase latency tracking
│   ├── db/
│   │   ├── session.py                   SQLAlchemy session
│   │   └── models.py                    Document chunk ORM models
│   ├── schemas/
│   │   ├── ingest.py
│   │   └── query.py
│   └── services/
│       ├── ingestion.py                 Chunking and preprocessing
│       ├── embedding.py                 SentenceTransformers inference
│       ├── retrieval.py                 pgvector similarity search
│       ├── langchain_retriever_service.py  LangChain abstraction layer
│       ├── direct_llm_service.py        Direct Ollama generation
│       ├── web_search_service.py        Tavily integration
│       ├── llm_service.py               LLM inference interface
│       ├── prompt_service.py            Context injection and prompt building
│       └── langgraph_agent_service.py   Agent graph and routing logic
├── scripts/
│   ├── init_db.py                       pgvector schema initialization
│   └── test_pipeline.py                 End-to-end smoke test
├── requirements.txt
├── docker-compose.yml
└── .env.example
```

---

## 🗺️ Roadmap

- [ ] **Hybrid search** — BM25 keyword search combined with vector search for improved recall on exact-match queries
- [ ] **Cross-encoder reranking** — second-pass reranking of retrieved chunks for precision improvement
- [ ] **RAGAS evaluation** — automated faithfulness, answer relevance, and context precision scoring on test query sets
- [ ] **Conversation memory** — multi-turn query sessions with LangGraph state persistence
- [ ] **Redis response caching** — cache frequent query responses to reduce LLM inference calls
- [ ] **Multi-format ingestion** — `.docx`, `.md`, and web URL support
- [ ] **Cloud LLM fallback** — OpenAI-compatible endpoint as alternative to local Ollama
- [ ] **API authentication** — API key middleware for endpoint protection

---

## 📝 License

MIT License

---

> Built as a production-style Agentic RAG platform demonstrating LangGraph state-machine orchestration, LangChain-compatible pgvector retrieval with HNSW indexing, local LLM inference via Ollama, and Tavily-powered real-time web search — with intelligent routing that eliminates unnecessary retrieval for every query.