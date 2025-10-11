# pylint: disable=C0114
from fastapi import APIRouter, status, HTTPException, Depends, Request
from core.telegram import (
    BotWebhook,
    BotMessageInput,
    TelegramBot
)
from core.logger import LOG
from api.ai import ask_gemini

router = APIRouter(prefix="/telegram", tags=["telegram"])

async def get_bot(request: Request) -> TelegramBot:
    """Get state of the bot from main app"""
    return request.app.state.bot

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook(payload: BotMessageInput, bot: TelegramBot=Depends(get_bot)):
    """Endpoint where telegram will send the data to."""
    message = None
    # photo = None
    LOG.info("receiving new payload \n %s", payload)
    chat_id = payload.message.chat.id

    if payload.message.entities:
        pass # come here if it is a command

    if payload.message.text:
        user_parts = {
            "role": "user",
            "content": payload.message.text
        }
        try:
            resp = ask_gemini(user_parts)
            msg = resp.choices[0].message.content

            await bot.send_message_to_bot(chat_id, message=msg)
        except Exception as e:
            raise HTTPException(500, detail=str(e)) from e

    if payload.message.text:
        if payload.message.caption:
            pass # here we will check if it has caption
        else:
            pass

    if payload.message.document:
        if payload.message.caption:
            pass # here we will check if it has caption
        else:
            pass


    msg = await bot.send_message_to_bot(chat_id, message=message)
    return msg

@router.post("/set_webhook", status_code=status.HTTP_200_OK)
async def set_telegram_webhook(dto: BotWebhook, bot: TelegramBot=Depends(get_bot)):
    """Set the telegram webhook to new webhook"""
    url = dto.url

    # always use try catch block
    try:
        curr_webhook = await bot.get_current_webhook()
        # first, we need to check if there is an active webhook
        if curr_webhook.get("result").get("url"):
            raise HTTPException(
                400,
                """
                There is an active webhook attached to the bot. Delete it first!
                """
            )

        # only set the webhook when there is no active webhook attached
        is_webhooked = await bot.set_webhook(url)
        if not is_webhooked:
            raise HTTPException(400, "Bad Request!")

        return {
            'status': "Success",
            'message': f"You have successfully attach {url} to the bot!",
            'status_code': status.HTTP_200_OK
        }

    except Exception as e:
        raise e

@router.get("/get_webhook", status_code=status.HTTP_200_OK)
async def get_telegram_webhook(bot: TelegramBot=Depends(get_bot)):
    """Get telegram webhook connected to the bot"""
    try:
        curr_webhook = await bot.get_current_webhook()
        if not curr_webhook.get("result").get("url"):
            raise HTTPException(404)

        return curr_webhook

    except Exception as e:
        raise e

@router.get("/delete_webhook", status_code=status.HTTP_200_OK)
async def delete_telegram_webhook(bot: TelegramBot=Depends(get_bot)):
    """Delete the webhook connected to the bot"""
    try:
        res = await bot.delete_webhook()
        return {'message': res.get("description"), 'status_code': status.HTTP_200_OK}
    except Exception as e:
        raise e
