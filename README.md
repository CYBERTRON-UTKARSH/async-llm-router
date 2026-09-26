# Nexus Gateway — Enterprise-Grade LLM Router & API Gateway

An OpenAI-compatible API gateway proxy that dynamically routes user prompts based on complexity, executes fallbacks on API errors, scrubs PII, and caches responses.

## Key Features
- **OpenAI Compatible Endpoint:** `/v1/chat/completions`
- **Dynamic Routing:** Routes lightweight queries to gemini()
- **Automatic Fallback:** Gracefully fails over to a secondary provider during outages or rate limits.
- **Inbound Guardrails:** Scrubs emails, phone numbers, and credit cards using regex filters.
- **Response Caching:** Caches response payloads in Redis to eliminate duplicate API costs.

## Local Setup
1. Clone repo & create virtualenv: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Add API keys in `.env`
4. Start Server: `uvicorn main:app --reload`