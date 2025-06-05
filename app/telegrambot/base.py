import requests
from utils.logger import get_logger
from utils import getsecret

logger = get_logger(__file__)

TOKEN = getsecret.get("TELEGRAM_BOT_API")

class TelegramBot:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"
        # self.send_message('890642031',"Bot Started")

    def send_request(self, method, data):
        url = self.base_url + method
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise an error for bad status codes
            logger.info("Message sent successfully: %s", response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error sending message: %s", e)
            return "Failed Request to TG API"

    def send_message(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text, "parse_mode": "Markdown"}
        return self.send_request('sendMessage', data)

    def reply_message(self, chat_id, msg_id, text):
        data = {
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': msg_id
        }
        return self.send_request('sendMessage', data)

    def send_photo(self, file_loc, caption, chat_id):
        with open(file_loc, "rb") as image_file:
            # Prepare data for the POST request (multipart form data)
            files = {
                "chat_id": (None, chat_id),
                "photo": (image_file.name, image_file, "image/jpeg"),
                "caption": (None, caption)
            }

            return requests.post(self.base_url + 'sendPhoto', files=files)
    
bot = TelegramBot(TOKEN)


class Message:
    def __init__(self, data):
        self.update_id = data.get('update_id')
        message = data.get('message', {})
        self.message_id = message.get('message_id')
        self.from_user = message.get('from', {})
        self.chat = message.get('chat', {})
        self.date = message.get('date')
        self.text = message.get('text')
        self.entities = message.get('entities', [])

        self.chat_id = self.chat.get('id')
        self.user_id = self.from_user.get('id')
        self.user_first_name = self.from_user.get('first_name')
        self.user_username = self.from_user.get('username')
        self.user_language_code = self.from_user.get('language_code')

        self.is_mention = any(
            entity.get('type') == 'mention' for entity in self.entities)
        self.is_command = any(
            entity.get('type') == 'bot_command' for entity in self.entities)
        self.is_simple_message = not self.entities