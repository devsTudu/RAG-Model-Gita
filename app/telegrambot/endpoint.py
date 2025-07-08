from fastapi import APIRouter, HTTPException

from .base import TelegramUpdate, BOT
from .helpers import update_handler


telegram_bot_router = APIRouter(prefix="/telegram")


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
            "allowed_updates": ["message",
                                "callback_query"
                                ]
            }
        response = BOT.send_request("setWebhook", webhook_data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to set webhook: {str(e)}")
    return response


@telegram_bot_router.post("/respond")
async def responder(update: TelegramUpdate):
    """Endpoint to handle incoming Telegram messages

    Args:
        query (Request): The Request object containing
        the incoming message data
    Raises:
        HTTPException: If the message does not contain text or
            if there is an error processing the message

    Returns:
        None : _description_
    """
    return await update_handler(update, BOT)


# chatid = 7964021486
