# Containerized ML Translation Service (MLOps)

A lightweight, self-contained machine learning microservice that serves an NLP Seq2Seq translation model (`Helsinki-NLP/opus-mt-en-de`) using FastAPI, Hugging Face Transformers, and Docker.

---

## Architecture Overview

```text
[ Client (Browser / cURL) ]
             │
             │ HTTP (Port 8000)
             ▼
┌────────────────────────────────────────────────────────┐
│               Docker Container (:8000)                 │
│                                                        │
│  FastAPI Application (app.py)                          │
│  ├── GET  /          -> Minimal Web UI                 │
│  ├── GET  /health    -> Liveness Check                 │
│  └── POST /translate -> Model Inference Endpoint       │
│                                │                       │
│                                ▼                       │
│  Hugging Face Pipeline (Cached Seq2Seq Model Weights)  │
│  Engine: PyTorch (CPU-optimized)                       │
└────────────────────────────────────────────────────────┘
