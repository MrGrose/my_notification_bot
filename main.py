import logging
import time
import requests

from telegram import ParseMode
from telegram import Bot
from typing import Optional, Any
from environs import Env
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def long_polling(logger: logging.Logger, dev_token: str, bot: Bot, tg_chat_id: int) -> None:
    logger.info("Бот запущен")
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": dev_token}
    params = {"timestamp": None}

    while True:
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=91
            )
            response.raise_for_status()
            checks_lesson = response.json()

            new_timestamp = process_lesson_attempts(checks_lesson, bot, tg_chat_id)
            if new_timestamp:
                params["timestamp"] = new_timestamp

        except ReadTimeout as error:
            logger.error(f"Ошибка получения ответа от сервера: {error}")
        except ConnectionError as error:
            logger.error(f"Ошибка подключения к интернету: {error}")
            time.sleep(30)
        except HTTPError as http_err:
            logger.error(f"Ошибка на стороне сервера: {http_err.response.status_code}")
        except Exception as e:
            logger.error(f"Произошла неизвестная ошибка: {e}")


def process_lesson_attempts(checks_lesson: dict, bot: Bot, tg_chat_id: int) -> Optional[Any | None]:
    if checks_lesson.get("timestamp") == "timeout":
        return checks_lesson.get("timestamp_to_request")
    else:
        new_attempts = checks_lesson.get("new_attempts")

        if new_attempts and len(new_attempts) > 0:
            attempt = new_attempts[0]
            lesson_title = attempt.get("lesson_title")
            is_negative = attempt.get("is_negative")
            lesson_url = attempt.get("lesson_url")

            send_message(
                bot,
                tg_chat_id,
                lesson_title,
                is_negative,
                lesson_url
            )

        return checks_lesson.get("last_attempt_timestamp")


def send_message(bot: Bot, tg_chat_id: int, lesson_title: str, is_negative: bool, lesson_url: str) -> None:
    check_lesson = f"*У вас проверили работу.*\n*{lesson_title}*\n{lesson_url}\n✅Преподавателю все понравилось, можно приступать к следущему уроку!"
    not_check_lesson = f"*У вас проверили работу.*\n*{lesson_title}*\n{lesson_url}\n❌К сожалению, в работе нашлись ошибки."

    bot.send_message(
        text=not_check_lesson if is_negative else check_lesson,
        chat_id=tg_chat_id,
        parse_mode=ParseMode.MARKDOWN,
    )


def main():
    env = Env()
    env.read_env()
    dev_token = env.str("DEV_TOKEN")
    tg_token = env.str("TG_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")
    bot = Bot(token=tg_token)

    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))

    long_polling(logger, dev_token, bot, tg_chat_id)


if __name__ == '__main__':
    main()
