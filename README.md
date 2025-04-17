# Telegram-бот для проверки работ на курсах Devman


## Описание

Этот простой бот помогает получать уведомления о проверенных работах на курсах Devman.




## Установка: 
1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd <directory>
   ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Запустить скрипт:
    ```bash
    python main.py
    ```


## Настройка
Необходимо создать `.env` файл:

    ```bash 
    DEV_TOKEN=ваш_токен
    TG_BOT_TOKEN=ваш_токен
    TG_CHAT_ID=ваш_токен
    ```
    
- [TG_BOT_TOKEN](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) для работы с телеграмм ботом.
- [DEV_TOKEN](https://dvmn.org/) необходимо зарегестрироваться и получить свой API токен.
- [TG_CHAT_ID]() @userinfobot данный бот покажет ваш id.