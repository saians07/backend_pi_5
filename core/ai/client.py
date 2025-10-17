# pylint: disable=W0718
"""
Client module to handle basic AI thing
"""
from openai import AsyncOpenAI
from core.logger import LOG
from core.ai.schema import OpenAIStandardResponse, OpenAIOutput, OpenAIContent

BASE_URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/"
BASE_URL_OPEN_ROUTER = "https://openrouter.ai/api/v1"


async def base_command(model: str, user_parts: dict, \
    system_prompt: str, client: AsyncOpenAI) -> OpenAIStandardResponse:
    """Base command as a template for another AI function"""
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                user_parts,
            ]
        )
        final_resp = OpenAIStandardResponse(
            id=resp.id,
            model=resp.model,
            output=OpenAIOutput(
                type="message",
                status="completed" if resp.choices[0].finish_reason == 'stop' else None,
                role=resp.choices[0].message.role,
                content=OpenAIContent(
                    type="output_text",
                    text=resp.choices[0].message.content,
                    annotations=resp.choices[0].message.annotations
                )
            )
        )
    except Exception as e:
        final_resp = OpenAIStandardResponse(
            model=model,
            output=OpenAIOutput(
                type="message",
                content=OpenAIContent(
                    type="output_text",
                    text="Maaf saat ini sedang ada gangguan Internal.\
                        Silahkan coba beberapa saat lagi."
                )
            )
        )
        LOG.info("%s", str(e))

    return final_resp
