import pytest

from app.telegrambot.user_details import (
    add_record,
    add_user,
    check_user_exists,
    remove_user,
)
from app.telegrambot.base import BOT


def test_user_details():
    user_name = "test_user"
    phone = "1234567890"
    chat_id = "1234567890"
    remove_user(chat_id)

    assert not check_user_exists(chat_id), "User already exists"
    assert (
        add_record(chat_id, user_name, phone) == 0
    ), "Record added for user non registered"
    add_user(user_name, phone, chat_id)
    assert check_user_exists(chat_id), "User not added"
    remove_user(chat_id)
    assert not check_user_exists(chat_id), "User not removed"


def test_bot_initialization():
    assert BOT is not None, "Bot initialization failed"
    assert hasattr(BOT, "send_message"), "Bot does not have send_message method"
    assert hasattr(BOT, "send_request"), "Bot does not have send_request method"

    assert (
        BOT.send_message(890642031, "Test message") is not None
    ), "Failed to send test message"
