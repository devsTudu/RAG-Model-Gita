import requests
from fastapi import APIRouter, Request, HTTPException

from .base import bot,Message



telegram_bot_router = APIRouter(prefix='/telegram')

@telegram_bot_router.get("/setwebook")
def setwebhook(url: str):
    """
    Set webhook for Telegram bot
    Args:
        url (str): The URL where Telegram will send updates
    """
    try:
        webhook_data = {
            "url": url,
            "allowed_updates": ["message", "callback_query"]
        }
        response = bot.send_request('setWebhook',
                         webhook_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to set webhook: {str(e)}"
        )
    return response

@telegram_bot_router.post("/respond")
async def responder(query:Request):
    msg = Message(query.body)
    return bot.send_message(msg.chat_id,"Hello")