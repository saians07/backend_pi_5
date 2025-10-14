# pylint: disable=C0114, W0511, R0912
from math import ceil
from fastapi import APIRouter
from core.telegram import (
    BotMessageInput,
    BotMessage,
    BotEntities,
    TelegramBot
)
from core.ai import (
    BOT_NAME,
    BOT_NICKNAME,
)
from api.ai import ask_gemini

router = APIRouter(prefix="/telegram", tags=["telegram"])

async def bot_assistant(payload: BotMessageInput, bot: TelegramBot) -> None:
    """
        Process all input from users.
        Return only string data, None when there is no
    """
    if payload.message:
        await user_message_handler(payload.message, bot)

    return

async def user_message_handler(message:BotMessage, bot: TelegramBot) -> None:
    """
        Handle message from users. String only return
    """
    if message.chat:
        chat_id = message.chat.id
        if message.from_.username:
            name = message.from_.username
        else:
            name = message.from_.first_name

        if message.entities:
            if message.entities.type_.find("start") >= 0:
                msg = f"Halo selamat datang. Aku {BOT_NAME} siap membantu kamu.\
                    Ada yang ingin ditanyakan? -- ❤️‍🔥 {BOT_NAME}"
                await bot.send_message_to_bot(chat_id, message=msg)

            return await user_command_handler(message.entities, name, bot, chat_id)

        if chat_id not in [683639588, 7703746371]:
            return f"Maaf, saat ini {BOT_NICKNAME} hanya melayani Berlin dan Swanti\
                saja. -- ❤️‍🔥 {BOT_NAME}"

        if message.text:
            msg = await text_message_handler(message)

            chunks = ceil(len(msg)/4000)
            for idx in range(0,chunks):
                idx_next = (idx + 1) * 4000 # telegram max accept 4000 character
                message = msg[(idx*4000):idx_next]
                if (idx+1) < chunks:
                    message += '--[Cont.]'
                await bot.send_message_to_bot(chat_id, message=message)

            return msg

async def text_message_handler(message:BotMessage) -> str:
    """Handling every text message from users"""
    user_parts = {
        "role": "user",
        "content": message.text
    }
    resp = await ask_gemini(user_parts)
    return resp.output.content.text

async def user_command_handler(
    entities: BotEntities, name: str, bot: TelegramBot, chat_id: int
) -> str:
    """Handling user command other than start"""
    if entities.type_ == "/help":
        msg = f"Halo {name}. Kamu bisa bertanya apa saja yang kamu \
            ingin tanyakan kepadaku! Aku, {BOT_NAME} akan berusaha bantu."

        await bot.send_message_to_bot(chat_id, message=msg)
