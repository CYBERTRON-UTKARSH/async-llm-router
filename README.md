# async-llm-router
Lightweight, OpenAI-compatible AI Gateway in Python using FastAPI &amp; httpx. Features in-flight guardrails, real-time PII redaction, prompt injection protection, and direct Groq LLM routing.
# async-llm-router

An OpenAI-compatible AI API Gateway built in Python using **FastAPI** and **`httpx`**, specifically designed to interface with **Groq's Ultra-Fast LPU Infrastructure**. It sits between client applications and Groq's cloud API to provide real-time security enforcement, PII scrubbing, and raw asynchronous HTTP routing without heavy vendor SDK dependencies.

---

## Key Features

* **Groq LPU Integration:** Direct high-speed routing to Groq's cloud endpoints (`llama-3.1`, `qwen`, etc.) with sub-100ms processing overhead.
* **In-Flight Guardrails:** Detects and blocks prompt injection and system override attempts at the perimeter, returning an HTTP `400 Bad Request` before calling upstream APIs.
* **Automated PII Redaction:** Uses regex pattern matching to scrub sensitive user data (emails, phone numbers) from prompt payloads in real-time.
* **Secret Leak Prevention:** Blocks prompts containing accidental API key or credential exposures (e.g., `gsk_`, `sk-`).
* **SDK-Free Transport:** Utilizes non-blocking asynchronous HTTP calls (`httpx.AsyncClient`) for full control over headers, connection timeouts, and payload structures.
* **OpenAI API Compatibility:** Exposes standard `/v1/chat/completions` endpoints for drop-in compatibility with existing LLM tools and frontend clients.

---

## System Architecture


 Client Application / Terminal
            │
            │ POST /v1/chat/completions
            ▼
  ┌───────────────────┐
  │   FastAPI Server  │  (main.py)
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────┐
  │ Security Engine   │  (guardrails.py)
  │  - Jailbreak Check│
  │  - PII Redaction  │
  └─────────┬─────────┘
            │ (If clean)
            ▼
  ┌───────────────────┐
  │ Raw HTTP Router   │  (router.py)
  └─────────┬─────────┘
            │
            │ Async POST (httpx)
            ▼
  ┌───────────────────┐
  │  Groq Cloud API   │  (api.groq.com)
  └─────────┬─────────┘
