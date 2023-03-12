from configparser import ConfigParser
from typing import NamedTuple

import telegram

from redis import Redis
from telethon import TelegramClient


class ProgramSettings(NamedTuple):
    api_id: int
    api_hash: str
    client: TelegramClient
    chat_name: int
    searching_phrase: str
    minimal_price: int
    messages_limit: int
    redis: Redis
    telegram_alerts_bot: telegram.Bot
    alerts_bot_chats_ids: list


def initialize_settings():
    config = ConfigParser()
    config.read("config.ini", encoding="utf-8")

    api_id = config.getint(
        section="PARSER BOT SETTINGS",
        option="api_id"
    )
    api_hash = config.get(
        section="PARSER BOT SETTINGS",
        option="api_hash"
    )
    parsing_chat_id = config.getint(
        section="CHAT SETTINGS",
        option="parsing_chat_id"
    )
    minimal_price = config.getint(
        section="CHAT SETTINGS",
        option="minimal_price"
    )
    search_phrase = config.get(
        section="CHAT SETTINGS",
        option="search_phrase"
    )
    messages_limit = config.getint(
        section="CHAT SETTINGS",
        option="messages_limit"
    )

    telegram_alerts_bot_token = config.get(
        section="ALERTS BOT SETTINGS",
        option="bot_token"
    )
    telegram_alerts_chats_ids = config.get(
            section="ALERTS BOT SETTINGS",
            option="chats_ids"
        ).split(",")
    telegram_alerts_chats_ids = [
        chat_id for chat_id in telegram_alerts_chats_ids if chat_id
    ]

    redis_host = config.get(
        section="REDIS",
        option="host"
    )
    redis_port = config.getint(
        section="REDIS",
        option="port"
    )
    client = TelegramClient('anon', api_id, api_hash)
    redis = Redis(host=redis_host, port=redis_port)
    telegram_alerts_bot = telegram.Bot(telegram_alerts_bot_token)

    return ProgramSettings(
        api_id,
        api_hash,
        client,
        parsing_chat_id,
        search_phrase,
        minimal_price,
        messages_limit,
        redis,
        telegram_alerts_bot,
        telegram_alerts_chats_ids
    )
