import subprocess
import time
from telegram import Bot
from environs import Env


def is_service_active(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() == "active"
    except subprocess.CalledProcessError:
        return False


def main():
    env = Env()
    env.read_env()
    log_tg_token = env.str("LOG_TG_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")
    bot_log = Bot(token=log_tg_token)

    service_name = "bot.service"
    check_interval = 60

    bot_was_active = None

    active = is_service_active(service_name)
    if active:
        bot_log.send_message(chat_id=tg_chat_id, text="ℹ️ Скрипт запущен. Бот сейчас активен.")
    else:
        bot_log.send_message(chat_id=tg_chat_id, text="ℹ️ Скрипт запущен. Бот сейчас НЕ активен.")

    bot_was_active = active

    while True:
        active = is_service_active(service_name)
        if active and bot_was_active is False:
            bot_log.send_message(chat_id=tg_chat_id, text="✅ Бот снова активен!")
        elif not active and bot_was_active is not False:
            bot_log.send_message(chat_id=tg_chat_id, text="❌ Бот упал!")

        bot_was_active = active
        time.sleep(check_interval)


if __name__ == "__main__":
    main()