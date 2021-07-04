## Файл botConf.ini
Настройки для бота телеграм.
- `token` - токен для работы бота(даётся при создании бота)
- `sleepTime` - задержка перед следующим запросом бота на почту(в секундах)

## Файл mailConf.ini
Настройки для доступа бота к почте(обязательное условие: включённый IMAP на почте)
- `host` - IMAP сервер(обычно даётся при включении IMAP на самой почте)
- `username` - адрес почты
- `password` - пароль(обязательное условие: включённый IMAP на почте, даётся при включении IMAP)

## Файл TeleBot.py
Главный файл, запускает телеграм-бота.

## Файл MailParser
Сам скрипт для работы с почтой.

### Команды для бота:
- `/start` - начинает проверку почты на новые(непрочитанные) сообщения, проверяет через sleepTime, указанное в botConf.ini
- `/end` - заканчивает проверку почты на новые(непрочитанные) сообщения