import requests
from typing import Optional
from pydantic import BaseModel, Field

from utils.logger import get_logger
from utils.environmentVariablesHandler import get


logger = get_logger(__file__)


TOKEN = get("TELEGRAM_BOT_API")
# Define inner models first, as they are used by outer models


class User(BaseModel):
    """
    Represents a Telegram user or bot.
    https://core.telegram.org/bots/api#user
    """

    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = ""

    # IETF language tag of the user's system
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


class Chat(BaseModel):
    """
    Represents a chat in Telegram.
    https://core.telegram.org/bots/api#chat
    """

    id: int
    # Type of chat, can be “private”, “group”, “supergroup” or “channel”
    type: str
    # Title, for supergroups, channels and group chats
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Message(BaseModel):
    """
    Represents a message.
    https://core.telegram.org/bots/api#message
    """

    message_id: int
    from_user: User
    # Sender of the message; can be empty for messages sent to channels
    chat: Chat  # Conversation the message belongs to
    date: int  # Date the message was sent in Unix time
    text: Optional[str] = (
        None  # For text messages, the actual UTF-8 text of the message
    )


class TelegramUpdate(BaseModel):
    """
    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    https://core.telegram.org/bots/api#update
    """

    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    # Add other update types as needed for your bot's functionality:
    # inline_query: Optional[InlineQuery] = None
    # chosen_inline_result: Optional[ChosenInlineResult] = None
    # callback_query: Optional[CallbackQuery] = None
    # shipping_query: Optional[ShippingQuery] = None
    # pre_checkout_query: Optional[PreCheckoutQuery] = None
    # poll: Optional[Poll] = None
    # poll_answer: Optional[PollAnswer] = None
    # my_chat_member: Optional[ChatMemberUpdated] = None
    # chat_member: Optional[ChatMemberUpdated] = None
    # chat_join_request: Optional[ChatJoinRequest] = None


class TelegramBot:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"
        # self.send_message('890642031',"Bot Started")

    def send_request(self, method, data):
        url = self.base_url + method
        try:
            response = requests.post(url, json=data, timeout=1000)
            response.raise_for_status()  # Raise an error for bad status codes
            logger.log(0, "Message sent successfully: %s", response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error sending message: %s", e)
            return "Failed Request to TG API"

    def updateMessage(self, chat_id, msg_id, text):
        data = {
            "chat_id": chat_id,
            "message_id": msg_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        resp = self.send_request("editMessageText", data)
        if isinstance(resp, dict):
            if resp.get("ok"):
                return resp.get("result", {}).get("message_id")
            logger.error(
                "Failed to update message: %s", resp.get(
                    "description", "Unknown error")
            )
        return None

    def send_message(self, chat_id, text):
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        resp = self.send_request("sendMessage", data)
        if isinstance(resp, dict):
            if resp.get("ok"):
                return resp.get("result", {}).get("message_id")
            logger.error(
                "Failed to send message: %s",
                resp.get("description", "Unknown error"),
            )

        return None

    def reply_message(self, chat_id, msg_id, text):
        data: dict = {"chat_id": chat_id, "text": text,
                      "reply_to_message_id": msg_id}
        resp = self.send_request("sendMessage", data)
        if isinstance(resp, dict):
            if resp.get("ok"):
                return resp.get("result", {}).get("message_id")

            logger.error(
                "Failed to send message: %s", resp.get(
                    "description", "Unknown error")
            )

    def send_photo(self, file_loc, caption, chat_id):
        with open(file_loc, "rb") as image_file:
            # Prepare data for the POST request (multipart form data)
            files = {
                "chat_id": (None, chat_id),
                "photo": (image_file.name, image_file, "image/jpeg"),
                "caption": (None, caption),
            }

            return requests.post(
                url=self.base_url + "sendPhoto", files=files, timeout=50000
            )


BOT = TelegramBot(TOKEN)
