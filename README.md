# Инструмент для удаленного управление кучи баз данных

web приложение для удаленного управление удаленных баз данных dom.ru

## Важно

Для работы с oracle db нужно установить [клиент](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)

`/backend/servers.json` - конфиг с серверами

## dev запуск

`/backend директория`

Предварительно создав venv

```bash
sudo su
source /venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## vue project compile

Предварительно настроив `/frontend/src/config.js`

```bash
npm i
npm run serve
```

[Посмотреть активные таски](./TASKS.md)
