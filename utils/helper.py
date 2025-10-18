"""
    Universal helper functions
"""
import re

async def telegram_message_escaper(msg: str) -> str:
        """
            before sending the message to the users, we need to clean up the
            message by escaping reserved chracters. This function will only
            be called when the main formatter failed to parse the document.
        """
        reserved_chars = r'_*[]()~`>#+-=|{}.!'
        # reserved_chars = r'()>#+-=|{}.!*'
        escaped_chars = fr"([{re.escape(reserved_chars)}])"

        escaped_msg = re.sub(escaped_chars, r'\\\1', msg)

        return escaped_msg

async def telegram_formatting_encode(msg: str) -> str:
    """
        Smartly detect formatting characters and then encode them
    """
    text = re.sub(r'```(.*?)```', lambda m: f'⚫CODE⚫{m.group(1)}⚫/CODE⚫', msg, flags=re.DOTALL)

    text = re.sub(r'`([^`]+?)`', r'⚫INLINECODE⚫\1⚫/INLINECODE⚫', text)

    text = re.sub(r'^(\s*)\* ', r'\1⚫BULLET⚫ ', text, flags=re.MULTILINE)
    text = re.sub(r'^(\s*)- ', r'\1⚫BULLET⚫ ', text, flags=re.MULTILINE)

    text = re.sub(r'^(\s*)(\d+)\. ', r'\1⚫NUM⚫\2⚫/NUM⚫ ', text, flags=re.MULTILINE)

    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'⚫BOLDITALIC⚫\1⚫/BOLDITALIC⚫', text)
    text = re.sub(r'___(.+?)___', r'⚫BOLDITALIC⚫\1⚫/BOLDITALIC⚫', text)

    text = re.sub(r'\*\*(.+?)\*\*', r'⚫BOLD⚫\1⚫/BOLD⚫', text)
    text = re.sub(r'__(.+?)__', r'⚫BOLD⚫\1⚫/BOLD⚫', text)
    text = re.sub(r'^## (.+)$', r'*\1*\n', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'*▸ \1*', text, flags=re.MULTILINE)
    text = re.sub(r'^#{4,6} (.+)$', r'*• \1*', text, flags=re.MULTILINE)

    text = re.sub(r'(?<!\w)\*([^\*\s][^\*]*?[^\*\s])\*(?!\w)', r'⚫ITALIC⚫\1⚫/ITALIC⚫', text)
    text = re.sub(r'(?<!\w)_([^_\s][^_]*?[^_\s])_(?!\w)', r'⚫ITALIC⚫\1⚫/ITALIC⚫', text)

    return text

async def telegram_formatting_decode(msg: str) -> str:
    """
        Decode formatting characters perviously encoded.
    """
    text = re.sub(r'⚫CODE⚫(.*?)⚫/CODE⚫', r'```\1```', msg, flags=re.DOTALL)
    text = re.sub(r'⚫INLINECODE⚫(.*?)⚫/INLINECODE⚫', r'`\1`', text)

    text = text.replace('⚫BULLET⚫ ', '• ')

    text = re.sub(r'⚫NUM⚫(\d+)⚫/NUM⚫ ', r'\1\\. ', text)

    text = text.replace('⚫BOLDITALIC⚫', '*_')
    text = text.replace('⚫/BOLDITALIC⚫', '_*')

    text = text.replace('⚫BOLD⚫', '*')
    text = text.replace('⚫/BOLD⚫', '*')

    text = text.replace('⚫ITALIC⚫', '_')
    text = text.replace('⚫/ITALIC⚫', '_')

    return text

async def telegram_message_smart_escaper(msg: str) -> str:
    """
        before sending the message to the users, we need to clean up the
        message by escaping reserved chracters.
    """
    text = await telegram_formatting_encode(msg)

    text = await telegram_message_escaper(text)

    text = await telegram_formatting_decode(text)

    return text
