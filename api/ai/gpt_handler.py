"""
Handlder for GPT AI variants
"""
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from core.logger import LOG
from core.ai import (
    BASE_URL_OPEN_ROUTER,
    base_command
)
from core.ai.schema import OpenAIStandardResponse

load_dotenv()

OPEN_ROUTER_API = os.getenv("OPENROUTERAPI")

if not OPEN_ROUTER_API:
    LOG.info("tidak ada key GEMINI_API_KEY di environment!")

async def ask_gpt_oss_20_b(user_parts: dict, system_prompt: str=None) -> OpenAIStandardResponse:
    """Execute function to call gpt oss from open router."""
    LOG.info("Asking GPT-OSS...")
    openai_client = AsyncOpenAI(
        base_url=BASE_URL_OPEN_ROUTER, api_key=OPEN_ROUTER_API
    )
    resp = await base_command(
        model="openai/gpt-oss-20b:free",
        system_prompt=system_prompt,
        user_parts=user_parts,
        client=openai_client
    )
    LOG.info("GPT-OSS done answering.")
    return resp
