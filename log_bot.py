import time
from telegram import Bot
from environs import Env


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(1)
            continue
        yield line


def main():
    env = Env()
    env.read_env()
    log_tg_token = env.str("LOG_TG_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")
    log_file_path = env.str("LOG_FILE_PATH", "bot.log")

    bot_log = Bot(token=log_tg_token)

    with open(log_file_path, "r", encoding="utf-8") as logfile:
        loglines = follow(logfile)
        for line in loglines:
            if "ERROR" in line or "CRITICAL" in line:
                try:
                    bot_log.send_message(chat_id=tg_chat_id, text=line)
                except Exception as e:
                    print(f"Ошибка отправки лога: {e}")


if __name__ == "__main__":
    main()