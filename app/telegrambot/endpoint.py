from fastapi import APIRouter, HTTPException
from utils.getsecret import get

from pprint import pprint
from .base import TelegramUpdate, TelegramBot
from .supabase import check_user_exhists,add_user, add_record
from src.agents.responder import get_quick


TOKEN = get("TELEGRAM_BOT_API")
BOT = TelegramBot(TOKEN)

telegram_bot_router = APIRouter(prefix='/telegram')
ACTIVATION_CODE = get("TELEGRAM_ACTIVATION_CODE")

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
        response = BOT.send_request('setWebhook',
                         webhook_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to set webhook: {str(e)}"
        )
    return response

async def send_response(chat_id: int, text: str):
    """Send a response to a specific chat ID"""
    msg_id = BOT.send_message(chat_id, "thinking")
    print(msg_id)
    try:
        resp = await get_quick(text)
        data = {
            "chat_id": chat_id,
            "text": resp,
            "message_id": msg_id,
            "parse_mode": "Markdown"
        }
        BOT.send_request("editMessageText",data)
        add_record(chat_id,text,resp)
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {str(e)}")

@telegram_bot_router.post("/respond")
async def responder(update:TelegramUpdate):
    """Endpoint to handle incoming Telegram messages

    Args:
        query (Request): The Request object containing the incoming message data
    Raises:
        HTTPException: If the message does not contain text or if there is an error processing the message

    Returns:
        None : _description_
    """
    
    msg_text = update.message.text if update.message else None
    sender = update.message.from_user.id
    username = update.message.from_user.username
    if msg_text == "/start":
        # If the message is "/start", send a welcome message
        return BOT.send_message(sender, "Welcome to the bot! Please provide the activation code to register.")
    
    # Respond if registered user sends a message
    if check_user_exhists(sender) and msg_text != ACTIVATION_CODE:
        await send_response(sender, msg_text)
        return BOT.send_message(sender,"Success")

    # Handle activation code
    return handle_activation_code(msg_text, sender, username)

def handle_activation_code(code: str, sender: int,username: str):    
    if msg_text == ACTIVATION_CODE:
        # If the activation code matches, register the user
        if check_user_exhists(sender):
            return BOT.send_message(sender, "You are already registered, you can ask questions")
        # Register the user in the database
        add_user(username, "123456879", sender)
        return BOT.send_message(sender, "You have been registered successfully, Start using the bot")
    
    return BOT.send_message(sender, "Invalid activation code.")
    
