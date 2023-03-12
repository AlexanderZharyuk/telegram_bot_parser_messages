import asyncio

from telethon import TelegramClient

from misc import initialize_settings


async def parse_messages(
        client: TelegramClient,
        chat_name: str,
        search_phrase: str
) -> list:
    """
    Parse messages from chat and return list of unique messages
    """
    await client.connect()

    messages = await client.get_messages(
        -1001218565226,
        search=search_phrase,
        limit=5
    )
    await client.disconnect()
    return messages


async def main():
    settings = await initialize_settings()
    messages = await parse_messages(
        client=settings.client,
        chat_name=settings.chat_name,
        search_phrase=settings.searching_phrase
    )
    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
