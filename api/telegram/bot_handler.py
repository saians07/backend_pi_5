from fastapi import APIRouter, status, HTTPException, Depends # pylint disable: C0114
import httpx
from core.telegram import (
    BotWebhook,
    BotMessageInput,
    TelegramBot
)

router = APIRouter(prefix="/telegram", tags=["telegram"])

def create_bot() -> TelegramBot:
    """Return a single shared bot instance"""
    client = httpx.AsyncClient()
    bot = TelegramBot(client)
    return bot

@router.post("/webhook", status_code=status.HTTP_200_OK)
def telegram_webhook(payload: BotMessageInput, bot: TelegramBot=Depends(create_bot)):
    """Endpoint where telegram will send the data to."""
    chat_id = payload.get("chat_id")
    message = payload

    msg = bot.send_message_to_bot(chat_id, message)
    return msg

@router.post("/set_webhook", status_code=status.HTTP_200_OK)
async def set_telegram_webhook(dto: BotWebhook, bot: TelegramBot=Depends(create_bot)):
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
async def get_telegram_webhook(bot: TelegramBot=Depends(create_bot)):
    """Get telegram webhook connected to the bot"""
    try:
        curr_webhook = await bot.get_current_webhook()
        if not curr_webhook.get("result").get("url"):
            raise HTTPException(404)

        return curr_webhook

    except Exception as e:
        raise e

@router.get("/delete_webhook", status_code=status.HTTP_200_OK)
async def delete_telegram_webhook(bot: TelegramBot=Depends(create_bot)):
    """Delete the webhook connected to the bot"""
    try:
        res = await bot.delete_webhook()
        return {'message': res.get("description"), 'status_code': status.HTTP_200_OK}
    except Exception as e:
        raise e
