# logic/openai_merger.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def merge_messages_with_audit(message_chain_text: str) -> str:
    """
    Merges MT700/707/799 messages into a final MT700 with audit using GPT-4o.
    """
    try:
        print("[merge] Starting GPT-4o call...")
        print(f"[merge] Prompt length: {len(message_chain_text)}")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a trade finance and SWIFT message expert."
                },
                {
                    "role": "user",
                    "content": build_merge_prompt(message_chain_text)
                }
            ],
            temperature=0.3,
            max_tokens=3500
        )

        print("[merge] GPT-4o response received.")
        return response.choices[0].message.content

    except Exception as e:
        print(f"[merge] Error: {str(e)}")
        return f"❌ Error during merge: {str(e)}"

def build_merge_prompt(message_chain_text: str) -> str:
    """
    Builds a strict prompt to get raw MT700 and audit trail output.
    """
    return f"""
You are a SWIFT LC specialist.

Instructions:
- Apply all MT707 and MT799 changes to the original MT700 in correct sequence.
- Output strictly:
  1. The final MT700 message (full SWIFT format with field tags)
  2. A field-by-field audit trail (list or markdown table)
- Do NOT include:
  - Explanations, intros, summaries, markdown headers (e.g. ###)
  - Any extra sentences before or after

Begin directly with the MT700 message content.

### Message Sequence:
{message_chain_text}

[Begin Output Below]
"""