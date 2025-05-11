# logic/openai_generator.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_synthetic_messages(prompt: str) -> str:
    """
    Uses gpt-3.5-turbo to generate synthetic SWIFT messages from a prompt.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a trade finance expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating messages: {str(e)}"

def detect_message_type(text: str) -> str:
    """
    Classifies a SWIFT message as MT700 / MT707 / MT799 using GPT-4o.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in SWIFT messaging."},
                {"role": "user", "content": f"""Classify the following SWIFT message as one of:
- MT700 (Letter of Credit Issuance)
- MT707 (Amendment to MT700)
- MT799 (Correction/Free-format Message for LC)

Only reply with the message type code (e.g., MT700).

Message:
{text[:2500]}"""}
            ],
            temperature=0,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
