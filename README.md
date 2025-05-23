# Telegram-бот для проверки работ на курсах Devman


## Описание
Этот простой бот представляет собой Telegram-бота, который использует API сервиса dvmn.org для отслеживания результатов проверки домашних заданий. Бот постоянно опрашивает API с помощью long polling и отправляет уведомления в Telegram-чат о том, была ли работа проверена и сдалась ли она успешно или с ошибками.
Для мониторинга работоспособности основного бота используется отдельный скрипт, который проверяет его статус через systemd и отправляет уведомления в случае проблем.

## Функциональность
`bot.py`
- Подключение к API dvmn.org с использованием long polling для получения обновлений о проверках домашних заданий.
- Обработка ответа сервера и определение результата проверки.
- Отправка уведомлений в Telegram с информацией о названии урока, ссылкой на работу и результатом проверки (успешно или с ошибками).
- Логирование событий и ошибок для удобства отладки, отправки в бота.

`log_bot.py`
- Мониторинг основного бота (`bot.py`) через systemd.
- Проверка статуса сервиса `bot.service`.
- Отправка уведомлений в Telegram-чат об изменении статуса основного бота (запущен, упал, перезапущен).

## Структура кода 
`bot.py`

- `poll_lesson_reviews()` — основная функция, реализующая long polling с API и обработку ошибок.

- `process_lesson_attempts()` — функция обработки полученной информации о проверке и вызова отправки сообщения.

- `send_message()` — формирует и отправляет сообщение в Telegram.

- `main()` — точка входа, считывает переменные окружения, инициализирует бота и запускает процесс опроса API.

`log_bot.py`

- `is_service_active()` - функция проверяет, активен ли systemd-сервис с именем `service_name`.

-  `main()` - точка входа, считывает переменные окружения, инициализирует бота, запускает мониторинг статуса основного бота.

## Требования
- Python 3.10 и выше

- Библиотеки:
    - requests
    - python-telegram-bot (Telegram Bot API)
    - environs (для работы с переменными окружения)
    - logging (входит в стандартную библиотеку)


## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd <directory>
   ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```


3. Создайте файл .env в той же директории, где находится main.py, и добавьте в него следующие переменные:

    ```bash 
    DEV_TOKEN=ваш_токен_для_API_dvmn
    TG_TOKEN=токен_вашего_бота_в_Telegram
    TG_CHAT_ID=ID_чата_в_Telegram_для_уведомлений
    LOG_TG_TOKEN=токен_лог-бота_в_Telegram
    ```
    
- [TG_BOT_TOKEN](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) для работы с телеграмм ботом.
- [DEV_TOKEN](https://dvmn.org/) необходимо зарегестрироваться и получить свой API токен.
- [TG_CHAT_ID]() @userinfobot данный бот покажет ваш id.

## Использование
Запустите скрипт командой:

```bash
python bot.py
python log_bot.py
```


Бот начнет работу, подключится к API dvmn.org и будет отправлять уведомления в указанный Telegram-чат при появлении новых результатов проверки домашних заданий.
