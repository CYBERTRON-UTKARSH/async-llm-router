Project Structure

├── config.py         # Environment configuration and API key sanitization
├── guardrails.py     # Regex security patterns and custom guardrail exceptions
├── router.py         # Raw async httpx execution layer and Groq endpoint caller
├── main.py           # FastAPI server and central exception management
├── test_gateway.py   # Terminal test script for verifying gateway behavior
└── .env              # Local environment file storing GROQ_API_KEY

# Getting Started with async-llm-router

This guide covers everything you need to set up, configure, run, and test **async-llm-router** locally.

---steps for running project

## 1. Prerequisites

Ensure you have the following installed on your machine:
* **Python 3.10+**
* **Git**
* A **Groq API Key** (obtainable for free from [console.groq.com](https://console.groq.com))

---

## 2. Installation & Environment Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/CYBERTRON-UTKARSH/async-llm-router.git](https://github.com/CYBERTRON-UTKARSH/async-llm-router.git)
   cd async-llm-router
