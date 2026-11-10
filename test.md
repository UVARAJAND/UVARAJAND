# Uvarajan D

**AI Integration & Automation Engineer**  
**Backend Developer · System Design**

Building scalable AI-powered products from Cuddalore, India.

[Portfolio](https://uvarajan-d.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/uvarajan-dev) · [Telegram](https://t.me/uvarajand) · [Email](mailto:uvarajandev@gmail.com)

> Open to AI / Backend roles

---

## What I Do

- Integrating LLMs into production backends
- Designing event-driven automation pipelines
- Building with FastAPI, PostgreSQL, Redis and Celery
- Working with RAG, agentic workflows and tool calling
- Designing systems for AI-powered products

## Whoami

```yaml
name: Uvarajan D
role: AI Integration & Automation Engineer
focus: Backend Development / System Design
location: Cuddalore, India
stack: Python · FastAPI · PostgreSQL
building: AI-powered products & automation
contact: uvarajandev@gmail.com
status: Open to AI / Backend roles
```

### Current Focus

- AI integration & LLM APIs
- Workflow automation
- Backend architecture
- System design
- RAG & vector search
- Reliable API contracts

## What I Build

| Capability | Focus | Tools |
| --- | --- | --- |
| **AI Integration** | *Connect models to products — not demos.* LLM APIs, streaming and fallbacks; RAG pipelines and vector search; tool/function calling; prompt, context and cost control. | OpenAI · Groq · Gemini · Pinecone |
| **Automation** | *Remove manual steps from the critical path.* Event and webhook pipelines; queues and scheduled jobs; idempotent, retry-safe workflows; failure handling and alerts. | Celery · Redis · Cron · Webhooks |
| **Backend & System Design** | *Services that stay correct under load.* API contracts, auth and validation; data modeling and storage; caching, scaling and isolation; logs, metrics and observability. | FastAPI · PostgreSQL · Docker · JWT |

## System Architecture

```text
Client / Webhook
      │
      ▼
FastAPI Backend
      │
      ▼
Queue + Workers
      │
      ▼
AI Layer
      │
      ▼
Data Layer
```

| Layer | Responsibility |
| --- | --- |
| Client / Webhook | HTTP requests, events and schedules |
| FastAPI Backend | Auth and validation, rate limits |
| Queue + Workers | Celery and Redis, retries and scheduling |
| AI Layer | LLM APIs and RAG, tools and fallbacks |
| Data Layer | Postgres and Pinecone, object storage |

**Async path:** AI Layer → Queue + Workers for streaming, retries and scheduled work.

> **How I think about it:** validate at the edge, enqueue the slow work, isolate every AI provider behind a contract, make retries idempotent, persist the result, and instrument the whole path.

## Selected Work

### 01 · Observe AI — Agentic Proctoring Platform

[Repository](https://github.com/UVARAJAND/Observe-AI---AI-Proctoring-and-Examination-Platform)

- Multi-service monorepo: FastAPI core API, React dashboards, PyQt6 proctoring client, Docker code-execution sandbox, LangGraph question morphing, JIT generation and report publishing.
- PostgreSQL on Neon for domain data, Supabase Storage for evidence and report artifacts, Groq as the primary LLM with Gemini fallbacks.
- JWT auth for web roles and HMAC-signed requests for the desktop client; signed telemetry flows through the report pipeline.
- Coordinates adaptive exams, isolated code execution and proctoring evidence end to end.

`Python` `FastAPI` `React` `PyQt6` `Docker` `LangGraph` `PostgreSQL` `Supabase`

### 02 · ALEC — Autonomous Legal Entity for Contracts

[Repository](https://github.com/UVARAJAND/Autonomous-Legel-Entity-for-Contracts)

> Team project — Code Blenders

- Risk analysis at clause level with BERT-large and SHAP explanations, plus summarization, company diligence and contract drafting services.
- Company diligence aggregates OpenCorporates, SerpAPI, AlphaVantage and NewsAPI into one reviewable report.
- RAG over Pinecone with All-MiniLM-L6-v2 embeddings; LLaMA 3.3 70B handles generation and drafting.
- Template-based and autonomous negotiation flows share one document and session store.

`React` `FastAPI` `MongoDB` `Pinecone` `BERT` `SHAP` `LLaMA 3.3 70B`

### 03 · Agentic RAG — Knowledge Retrieval

[Repository](https://github.com/UVARAJAND/AI-Powered-Knowledge-Retrieval-with-Agentic-RAG)

> Team project — Code Blenders

- Multi-agent RAG over the Bhagavad Gita and Yoga Sutras, with query refinement, semantic retrieval and a feedback loop.
- Pinecone stores Sentence Transformers embeddings; Llama 3.3 70B runs through Ollama for offline use or Groq for hosted inference.
- FastAPI application with SQLite session history and a JSON output format for traceable answers.
- Evaluated on a 46-question set spanning both source texts, with saved outputs for review.

`Python` `FastAPI` `Pinecone` `Sentence Transformers` `Llama 3.3` `Ollama` `Groq`

## Tech Stack

| Area | Tools |
| --- | --- |
| Languages / Backend | Python · FastAPI · Flask · PostgreSQL · MongoDB · SQLite · Redis · Celery · Docker · Git |
| AI / Automation | OpenAI · Groq · Gemini · LangGraph · RAG · Pinecone · Sentence Transformers · Ollama · Function Calling |
| Systems / Ops | REST APIs · Webhooks · JWT · HMAC · Supabase · Neon · Cron · Idempotency · Observability |

## GitHub Activity

- [Contribution graph](https://github.com/UVARAJAND?tab=overview)
- [Repositories](https://github.com/UVARAJAND?tab=repositories)
- [Pinned work](https://github.com/UVARAJAND)

---

*Uvarajan D · AI integration · Automation · Backend · System design*
