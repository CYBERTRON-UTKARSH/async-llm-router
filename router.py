import httpx
from config import GROQ_API_KEY
from guardrails import apply_input_guardrails, GuardrailException

async def route_and_execute(messages: list, req_model: str = None) -> dict:
    # 1. Run Guardrails
    try:
        sanitized_messages = apply_input_guardrails(messages)
    except GuardrailException as ge:
        return {
            "error": {
                "message": ge.message,
                "type": "guardrail_violation",
                "category": ge.category
            }
        }

    # 2. Send Raw HTTP Request directly to Groq
    return await _call_groq(sanitized_messages)

async def _call_groq(messages: list) -> dict:
    if not GROQ_API_KEY:
        return {"error": {"message": "GROQ_API_KEY is missing in .env!"}}

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen/qwen3.8-27b",
        "messages": messages
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, headers=headers, json=payload)
        
        if res.status_code != 200:
            print(f"\n[GROQ API ERROR {res.status_code}] {res.text}\n")
            return {
                "error": {
                    "message": f"Groq API returned HTTP {res.status_code}",
                    "details": res.text
                }
            }

        return res.json()