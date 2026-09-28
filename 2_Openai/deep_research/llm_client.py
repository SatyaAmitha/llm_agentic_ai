import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.openai import openai as lf_openai

load_dotenv(override=True)

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Prefer LLM_*; fall back to LOCAL_LLM_*; default to Ollama
LLM_BASE_URL = os.getenv("LLM_BASE_URL") or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("LOCAL_LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL") or os.getenv("LOCAL_LLM_MODEL", "llama3.2:latest")
client = lf_openai.AsyncOpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
print(f"Using model: {LLM_MODEL} @ {LLM_BASE_URL}")
