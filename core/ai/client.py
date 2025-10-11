from openai import OpenAI as openai

BASE_URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/"
BASE_URL_OPEN_ROUTER = "https://openrouter.ai/api/v1"


async def base_command(base_url: str, model: str, user_parts: dict, \
    system_prompt: str, api_key: str=None) -> dict:
    async with openai(
        base_url=base_url,
        api_key=api_key
    ) as client:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                user_parts,
            ]
        )

        return resp