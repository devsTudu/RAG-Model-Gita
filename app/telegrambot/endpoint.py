from fastapi import APIRouter, Request, HTTPException
from utils.getsecret import get

from .base import bot,Message
from .supabase import check_user_exhists,add_user, add_record
from src.agents.responder import get_quick

import threading

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
        response = bot.send_request('setWebhook',
                         webhook_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to set webhook: {str(e)}"
        )
    return response

def send_response(chat_id: int, text: str):
    """Send a response to a specific chat ID"""
    bot.send_message(chat_id, "thinking")
    try:
        resp = get_quick(text)
        bot.send_message(chat_id, resp)
        add_record(chat_id,text,resp)
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {str(e)}")

@telegram_bot_router.post("/respond")
async def responder(query:Request):
    """Endpoint to handle incoming Telegram messages

    Args:
        query (Request): The Request object containing the incoming message data
    Raises:
        HTTPException: If the message does not contain text or if there is an error processing the message

    Returns:
        None : _description_
    """
    msg = Message(await query.json())
    if not msg.text:
        return bot.send_message(msg.chat_id, "No text provided in the message.")
    # Checking Activation Code
    if msg.text != ACTIVATION_CODE and not check_user_exhists(msg.chat_id):
        # If the activation code does not match and the user does not exist, return an error message
        return bot.send_message(msg.chat_id, "Invalid activation code.")
    if msg.text == ACTIVATION_CODE:
        # If the activation code matches, register the user
        if check_user_exhists(msg.chat_id):
            return bot.send_message(msg.chat_id, "You are already registered.")
        # Register the user in the database
        add_user(msg.user_username, "123456879", msg.chat_id)
        return bot.send_message(msg.chat_id, "You have been registered successfully, Start using the bot")
    
    # If the message contains text, send a response
    try:
        
        th = threading.Thread(
            target=send_response,
            args=(msg.chat_id, msg.text),
            daemon=True
        )
        th.start()
    except Exception as e:
        return bot.send_message(msg.chat_id, f"Error processing your request: {str(e)}")
    