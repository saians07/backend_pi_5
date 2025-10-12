"""
Handlder for Gemini AI variants
"""
import os
from dotenv import load_dotenv
from core.logger import LOG
from core.ai import (
    BASE_PROMPT,
    BASE_URL_GEMINI,
    base_command
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    LOG.info("tidak ada key GEMINI_API_KEY di environment!")

async def ask_gemini(user_parts: dict, system_prompt: str=None):
    """Execute function to call gemini"""
    LOG.info("Asking Gemini...")
    resp = await base_command(
        base_url=BASE_URL_GEMINI,
        model="gemini-2.5-flash",
        api_key=GEMINI_API_KEY,
        system_prompt=BASE_PROMPT if not system_prompt else system_prompt,
        user_parts=user_parts
    )
    LOG.debug("Answer: %s", resp.choices[0])
    LOG.info("Gemini done answering.")
    return resp
