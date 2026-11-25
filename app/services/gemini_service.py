
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Find the project root and load its .env file
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def generate_ai_response(prompt):
    """Generate a response using Gemini."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


def generate_embeddings(texts, task_type):
    """Generate vector embeddings for text."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config={"task_type": task_type}
    )

    return [embedding.values for embedding in response.embeddings]
