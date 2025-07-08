from typing import Any, Dict
from postgrest import APIResponse
from supabase import create_client, Client

from utils.environmentVariablesHandler import get
from utils.logger import get_logger


logger = get_logger(__name__)


url: str = get("SUPABASE_URL")
key: str = get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def add_user(username, phone, chat_id):
    """
    Adds a new user in the database of user
    """
    _: APIResponse[Dict[str, Any]] = (
        supabase.table("telegram_user").insert(
            {"username": username, "phone": phone, "chat_id": chat_id}
        )
    ).execute()


def add_record(chat_id, query, response):
    """Add the discussion record of the user and our model"""
    try:
        supabase.table("telegram_messages").insert(
            {"chat_id": chat_id, "query": query, "response": response}
        ).execute()
        return 1
    except Exception as e:
        logger.error("Uploading messsage to server failed: %s", e)
        return 0


def check_user_exhists(chat_id):
    """Returns true if the user already exhists"""
    response = (
        supabase.table("telegram_user").select(
            "*").eq("chat_id", chat_id).execute()
    )
    return len(response.data) == 1


def remove_user(chat_id):
    """Remove the user's data and the messages"""
    supabase.table("telegram_user").delete().eq("chat_id", chat_id).execute()
