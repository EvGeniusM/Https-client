# Https-client

Авторы решения задачи: Гришин Егор, Мингалев Евгений

Описание: реализация HTTP(S) клиента, позволяющего выполнять запросы к указанным URL-адресам с использованием различных методов (GET, POST, PUT, DELETE) 
с возможнностью сохранения ответа в формате HTML.

Пример запуска: python main.py get https://ya.ru --save

Доступные команды:
GET: python main.py get <url> [--params <params>] [--headers <headers>] [--cookies <cookies>] [--save] [--timeout <timeout>]
POST: python main.py post <url> [--data <data>] [--headers <headers>] [--cookies <cookies>] [--json <json_data>] [--save] [--timeout <timeout>]
PUT: python main.py put <url> [--data <data>] [--headers <headers>] [--json <json_data>] [--save] [--timeout <timeout>]
DELETE: python main.py delete <url> [--headers <headers>] [--save] [--timeout <timeout>]
Help: python main.py help