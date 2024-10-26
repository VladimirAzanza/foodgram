# Настроить запуск проекта Foodgram в контейнерах и CI/CD с помощью GitHub Actions

Foodgram - социальная сеть для обмена рецепты на онлайн-платформе.
Кроме того, можно скачать список продуктов, необходимых для приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.

Часть учебного курса, но он создан полностью самостоятельно.

## Инструкция по настройке проекта

- Клонировать репозиторий локально:
```
git clone git@github.com:VladimirAzanza/foodgram.git
cd foodgram
```
- Настройте Dockerfile backend/frontend в соответсвии с вашими потребностями (Можете оставить настройки по умолчанию):
```
nano backend/Dockerfile
nano frontend/Dockerfile
```
- Настройте "infra" в соответствии с вашими потребностями для конфигурации Nginx (Можете оставить настройки по умолчанию):
```
nano nginx/Dockerfile
nano nginx/nginx.conf
```
- Настройте оркестрации контейнеры в соответствии с вашими потребностями (Можете оставить настройки по умолчанию):
```
nano docker-compose.production.yml
```
- Установите Docker на сервере:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```
- Создайте на сервере директорию foodgram:
```
mkdir foodgram
```
- Создайте в файл .env:

```
cd foodgram
touch .env
```
- Переменные среды
```
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь базы данных
- `POSTGRES_PASSWORD` - пароль
- `DB_HOST` - имя хоста базы данных
- `DB_PORT` - порт базы данных 5432
- `SECRET_KEY` - секретный ключ Джанго
- `DEBUG` - логическое значение True or False (в разработке)
- `ALLOWED_HOSTS` - домен1 домен2 localhost 127.0.0.1
- `DB_ENGINE` - SQLite (в разработке) или PostgreSQL
- `URL_TO_RECIPES` - recipes
- `FRONTEND_URL` - http://localhost:3000 or https://domain
- `CSRF_TRUSTED_ORIGINS` - https://domain
```
- Автоматизируйте CI/CD с помощью GitHub Actions (Можете оставить настройки по умолчанию):
```
nano .github/workflows/main.yml
```
- Добавьте секреты в GitHub Actions:
```
   DOCKER_USERNAME 
   DOCKER_PASSWORD
   HOST - Адрес IP
   USER - имя пользователя на сервере
   SSH_KEY
   SSH_PASSPHRASE
   TELEGRAM_TO - ID телеграм-аккаунта
   TELEGRAM_TOKEN - токен бота, можно его получить через @BotFather 
```
## Добавление ингредиентов в базу данных

В папке `data` есть файл CSV с более чем 2000 ингредиентов и единиц измерения. (Сначала скопируйте содержимое папки на сервер.) Вы можете добавить их в базу данных, используя команду:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_csv_data --path /data/ingredients.csv
```
Эта команда не была добавлена в задачи CI/CD на .github/workflows/main.yml, так как она выполняется один раз при запуске проекта или для того, чтобы владелец сервера мог создавать свои собственные ингредиенты.

## Настройте Nginx на сервере для прослушивания правильного порта: по умолчанию используется порт 8001

```
sudo nano /etc/nginx/sites-enabled/default
```

```
server {
    server_name <Ваш домен>;

    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8001;
    }
}
```
### Проверьте правильность конфигурации Nginx:

```
sudo nginx -t
```

### Перезапустите Nginx:
```
sudo service nginx reload
```

### Стек

Python 3.10
Django 4.2.16
Django Rest Framework 3.15.2
Gunicorn 20.1.0
Docker 27.3.1
PostgreSQL 13

