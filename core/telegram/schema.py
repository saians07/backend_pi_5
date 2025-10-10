from pydantic import BaseModel

class WebhookDTO(BaseModel):
    """Parsing Raw Webhook URL From User"""
    url: str