"""
Handlder for Gemini AI variants
"""
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from core.logger import LOG
from core.ai import (
    BASE_URL_GEMINI,
    base_command
)
from core.ai.schema import OpenAIStandardResponse

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    LOG.info("Tidak ada key GEMINI_API_KEY di environment!")
    raise RuntimeError("Tidak ada key GEMINI_API_KEY di environment.")

async def ask_gemini(user_parts: dict, system_prompt: str=None) -> OpenAIStandardResponse:
    """Call gemini model to answer our inquiry. String only return."""
    LOG.info("Asking Gemini...")
    openai_client = AsyncOpenAI(
        base_url=BASE_URL_GEMINI, api_key=GEMINI_API_KEY
    )

    resp = await base_command(
        model="gemini-2.5-flash",
        system_prompt=system_prompt,
        user_parts=user_parts,
        client=openai_client
    )
    LOG.info("Gemini done answering.")
    return resp
