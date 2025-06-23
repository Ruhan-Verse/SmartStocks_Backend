# app/services/llm/gemini.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

load_dotenv()  # Load from .env file

# Load Gemini API Key
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini client
genai.configure(api_key=GENAI_API_KEY)

# Load Gemini model (make sure this is a valid, supported model ID)
model = genai.GenerativeModel("gemini-1.5-flash")  # You can also use "gemini-1.5-pro"

# Async wrapper around sync model.generate_content()
async def generate(prompt: str) -> str:
    try:
        # Run the blocking model call in a separate thread to avoid blocking the event loop
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
