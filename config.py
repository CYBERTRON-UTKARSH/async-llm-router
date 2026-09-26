import os
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip('"\' ')
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379").strip('"\' ')