import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.5"))
GROQ_TOP_P = float(os.getenv("GROQ_TOP_P", "0.9"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "300"))

# Initialize Groq client
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

def ask_gemini(prompt: str) -> str:
    """
    Legacy function name kept for backward compatibility.
    Now uses Groq API instead of Gemini.
    """
    return ask_groq(prompt)

def ask_groq(prompt: str) -> str:
    """
    Send a prompt to Groq API and get a complete response (non-streaming).
    """
    if not GROQ_API_KEY:
        return "Configuration Error: GROQ_API_KEY is missing."
    
    if not client:
        return "Configuration Error: Groq client not initialized."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            top_p=GROQ_TOP_P,
            max_tokens=GROQ_MAX_TOKENS,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"GROQ API ERROR: {str(e)}"

def ask_groq_stream(prompt: str):
    """
    Send a prompt to Groq API and get a streaming response.
    Yields chunks of text as they arrive.
    """
    if not GROQ_API_KEY:
        yield "Configuration Error: GROQ_API_KEY is missing."
        return
    
    if not client:
        yield "Configuration Error: Groq client not initialized."
        return

    try:
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            top_p=GROQ_TOP_P,
            max_tokens=GROQ_MAX_TOKENS,
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"GROQ API ERROR: {str(e)}"