import re

class GuardrailException(Exception):
    def __init__(self, message: str, category: str = "SECURITY"):
        self.message = message
        self.category = category
        super().__init__(self.message)

JAILBREAK_PATTERNS = [
    r"ignore\s+all\s+previous\s+instructions",
    r"ignore\s+above\s+instructions",
    r"disregard\s+all\s+prior\s+prompts",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"reveal\s+system\s+prompt",
]

EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
API_KEY_PATTERN = r'\b(?:gsk_|sk-|AIzaSy)[a-zA-Z0-9_\-]{20,}\b'

def apply_input_guardrails(messages: list) -> list:
    sanitized = []
    for msg in messages:
        content = msg.get("content", "")
        role = msg.get("role", "user")

        # 1. Jailbreak Check
        for pattern in JAILBREAK_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                raise GuardrailException("Request blocked: Jailbreak or prompt injection detected.", category="PROMPT_INJECTION")

        # 2. Secret / API Key Leak Check
        if re.search(API_KEY_PATTERN, content):
            raise GuardrailException("Request blocked: Input contains sensitive API keys.", category="SECRET_LEAK_PREVENTION")

        # 3. PII Masking
        content = re.sub(EMAIL_PATTERN, "[REDACTED_EMAIL]", content)
        content = re.sub(PHONE_PATTERN, "[REDACTED_PHONE]", content)

        sanitized.append({"role": role, "content": content})

    return sanitized