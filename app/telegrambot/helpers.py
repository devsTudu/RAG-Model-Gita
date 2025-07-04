from .base import TelegramUpdate, TelegramBot
from .supabase import check_user_exhists,add_user, add_record
from src.agents.responder import get_quick
from utils.getsecret import get


ACTIVATION_CODE = get("TELEGRAM_ACTIVATION_CODE")


async def update_handler(update:TelegramUpdate, BOT: TelegramBot):
    """Handle incoming Telegram updates and messages."""
    msg_text = update.message.text if update.message else None
    sender = update.message.from_user.id
    username = update.message.from_user.username
    if msg_text == "/start":
        # If the message is "/start", send a welcome message
        return BOT.send_message(sender, "Welcome to the bot! Please provide the activation code to register.")
    
    # Respond if registered user sends a message
    if check_user_exhists(sender) and msg_text != ACTIVATION_CODE:
        await send_response(sender, msg_text,BOT,msg_id=update.message.message_id)
        return BOT.send_message(sender,"Completed your request, you can ask more questions")

    # Handle activation code
    return BOT.send_message(sender,handle_activation_code(msg_text, sender, username))

def handle_activation_code(code: str, sender: int,username: str):    
    if code == ACTIVATION_CODE:
        # If the activation code matches, register the user
        if check_user_exhists(sender):
            return "You are already registered, you can ask questions"
        # Register the user in the database
        add_user(username, "123456879", sender)
        return "You have been registered successfully, Start using the bot"
    
    return "Invalid activation code."
    

async def send_response(chat_id: int, text: str, BOT: TelegramBot, msg_id: int = None):
    """Send a response to a specific chat ID"""
    try:
        msg_id = BOT.reply_message(chat_id, msg_id, "thinking")
    except Exception as e:
        msg_id = BOT.send_message(chat_id, "thinking")
    
    try:
        resp = await get_quick(text)
        # print(f"Response for {chat_id}: {resp}, msg_id: {msg_id}")
        update_msg = BOT.updateMessage(chat_id, msg_id, resp)
        if not isinstance(update_msg,int):
            return BOT.send_message(chat_id, "Something went wrong, please try again later.")
        add_record(chat_id,text,resp)
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {str(e)}")
