from fastapi import APIRouter, status, HTTPException, Depends
import httpx
from core.telegram import (
    WebhookURL,
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
def telegram_webhook(payload: BotMessageInput):
    """Endpoint where telegram will send the data to."""
    return payload

@router.post("/set_webhook", status_code=status.HTTP_200_OK)
async def set_telegram_webhook(dto: WebhookURL, bot: TelegramBot=Depends(create_bot)):
    url = dto.url
    
    # always use try catch block
    try:
        curr_webhook = await bot.get_current_webhook()
        # first, we need to check if there is an active webhook
        if curr_webhook.get("result").get("url"):
            raise HTTPException(400, "There is an active webhook attached to the bot. Delete it first!")

        # only set the webhook when there is no active webhook attached
        is_webhooked = await bot.set_webhook(url)
        if is_webhooked:
            return {
                'status': "Success",
                'message': f"You have successfully attach {url} to the bot!",
                'status_code': status.HTTP_200_OK
            }
        else:
            raise HTTPException(400, "Bad Request!")
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/get_webhook", status_code=status.HTTP_200_OK)
async def get_telegram_webhook(bot: TelegramBot=Depends(create_bot)):
    try:
        curr_webhook = await bot.get_current_webhook()
        if curr_webhook.get("result").get("url"):
            return curr_webhook
        else:
            raise HTTPException(404, "No webhook found!")
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/delete_webhook", status_code=status.HTTP_200_OK)
async def delete_telegram_webhook(bot: TelegramBot=Depends(create_bot)):
    try:
        res = await bot.delete_webhook()
        return {'message': res.get("description"), 'status_code': status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(500, str(e))
