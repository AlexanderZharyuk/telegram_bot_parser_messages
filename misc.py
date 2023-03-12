from configparser import ConfigParser
from typing import NamedTuple

from telethon import TelegramClient


class ProgramSettings(NamedTuple):
    api_id: int
    api_hash: str
    client: TelegramClient
    chat_name: str
    searching_phrase: str
    minimal_price: int


async def initialize_settings():
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
    parsing_chat_id = config.get(
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
    client = TelegramClient('anon', api_id, api_hash)

    return ProgramSettings(
        api_id,
        api_hash,
        client,
        parsing_chat_id,
        search_phrase,
        minimal_price,
    )
