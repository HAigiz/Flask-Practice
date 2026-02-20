# Flask-Practice

- **Dockerfile** - Сборка приложения.
- **app.py** - Приложение с эндпоинтами, описанием базы данных и настройкой подключения к Redis.
- **docker-compose.yml** - Запуск PSQL, Redis, Web и Nginx.
- **nginx.conf** - Конфиг веб-сервера.
- **requirements.txt** - Библиотеки для Python.

### Проверка Nginx (HTTP-кеширование)
```bash
curl -I http://localhost/items
```

- Первый запрос: В ответе увидите `X-Proxy-Cache`: `MISS`. Это значит, Nginx сходил к Flask.
- Второй запрос (сразу за первым): Увидите `X-Proxy-Cache`: `HIT`. Это значит, Nginx отдал данные из своего кеша, даже не беспокоя бэкенд.


<img width="1056" height="391" alt="image" src="https://github.com/user-attachments/assets/b4449bf4-147e-47a3-98cf-491070c4ebd5" />


### Прорка CRUD и базы данных
**POST** запрос
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "My Notebook"}' http://localhost/items
```


<img width="1054" height="64" alt="image" src="https://github.com/user-attachments/assets/b780cd46-6cc6-4709-b93f-f366b6da667f" />


Затем проверим, что она в базе через **GET**
```bash
curl http://localhost/items
```


<img width="1052" height="63" alt="image" src="https://github.com/user-attachments/assets/9a000a3d-d586-4360-a720-2c3384c260ae" />


### Проверка Redis
```bash
docker-compose exec redis redis-cli keys "*"
```


<img width="1060" height="64" alt="image" src="https://github.com/user-attachments/assets/e89f4839-a229-4c9c-83ff-01bb5a955de4" />


Если Flask успешно сохранил данные, вы увидите список ключей типа `flask_cache_...`.
