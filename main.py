import asyncio
import logging

from datetime import datetime

from pickle import loads, dumps

import telethon.tl.types.messages
from telethon import TelegramClient

from misc import initialize_settings


logging_format = "[%(levelname)s] %(message)s"
logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def parse_messages(
        client: TelegramClient,
        chat_id: int,
        search_phrase: str,
        messages_limit: int
) -> list:
    """
    Parse messages from chat and return list of unique messages
    """
    await client.connect()
    messages = await client.get_messages(
        entity=chat_id,
        search=search_phrase,
        limit=messages_limit
    )
    await client.disconnect()

    return messages


async def filter_new_messages(
        messages: list[telethon.tl.types.Message],
        minimal_price: int
) -> list[str]:
    validate_messages = []
    for message_info in messages:
        message_text = message_info.message
        price_string_start_index = message_text.find("Цена:") + 5
        price_string_end_index = message_text[price_string_start_index:].find(
            "\n"
        ) + price_string_start_index

        date_string_start_index = message_text.find("Дата:") + 6
        date_string_end_index = message_text[date_string_start_index:].find(
            "\n"
        ) + date_string_start_index

        price = message_text[price_string_start_index:price_string_end_index]
        date = message_text[date_string_start_index:date_string_end_index]

        try:
            reformatted_datetime = datetime.strptime(
                date.strip(),
                "%d.%m.%Y"
            ).date()
        except ValueError:
            logger.error("Can't convert date to datetime")
            continue

        try:
            trip_price = int(price.strip())
        except ValueError:
            logger.error("Can't convert price to int")
            continue

        if trip_price >= minimal_price and reformatted_datetime >= datetime.now().date():
            validate_messages.append(message_info)

    validate_messages = [
            message_info.message for message_info in validate_messages
        ]
    return validate_messages


async def main():
    project_settings = initialize_settings()
    while True:
        await asyncio.sleep(15)
        logger.info(
            f"[{datetime.now().hour}:{datetime.now().minute}] Still working"
        )
        new_messages = await parse_messages(
            client=project_settings.client,
            chat_id=project_settings.chat_name,
            search_phrase=project_settings.searching_phrase,
            messages_limit=project_settings.messages_limit
        )
        validated_new_messages = await filter_new_messages(
            messages=new_messages,
            minimal_price=project_settings.minimal_price
        )

        if not validated_new_messages:
            continue

        try:
            old_messages = loads(project_settings.redis.get("old_messages"))
        except TypeError:
            old_messages = []

        if not old_messages:
            project_settings.redis.set(
                "old_messages",
                dumps(validated_new_messages)
            )
            for message in old_messages:
                for chat_id in project_settings.alerts_bot_chats_ids:
                    project_settings.telegram_alerts_bot.send_message(
                        chat_id=int(chat_id),
                        text=message
                    )
            continue

        if old_messages != validated_new_messages:
            not_sending_messages = set(validated_new_messages).difference(
                old_messages
            )

            for message in not_sending_messages:
                for chat_id in project_settings.alerts_bot_chats_ids:
                    project_settings.telegram_alerts_bot.send_message(
                        chat_id=int(chat_id),
                        text=message
                    )

            project_settings.redis.set(
                "old_messages",
                dumps(validated_new_messages)
            )
            continue


if __name__ == "__main__":
    asyncio.run(main())

