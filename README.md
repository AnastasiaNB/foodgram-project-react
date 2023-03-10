# foodgram-project-react

![badge](https://github.com/AnastasiaNB/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Cтек технологий:
- Python
- Django
- Django REST Framework 
- PostgreSQL 
- JWT
- Nginx 
- gunicorn 
- Docker 
- Docker-compose 
- DockerHub 
- GitHubActions 
- Yandex.Cloud

## Описание
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта:
#### В репозитории на Гитхабе добавьте данные в Settings - Secrets - Actions secrets:
- DOCKER_USERNAME - имя пользователя в DockerHub
- DOCKER_PASSWORD - пароль пользователя в DockerHub
- HOST - ip-адрес сервера
- USER - пользователь
- SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
- PASSPHRASE - кодовая фраза для ssh-ключа
- DB_ENGINE - django.db.backends.postgresql
- DB_HOST - db
- DB_PORT - 5432
- ALLOWED_HOSTS - список разрешённых адресов
- DB_NAME - postgres (по умолчанию)
- POSTGRES_USER - postgres (по умолчанию)
- POSTGRES_PASSWORD - postgres (по умолчанию)
- DJANGO_SUPERUSER_EMAIL - email для создание суперюзера
- DJANGO_SUPERUSER_USERNAME - логин для суперюзера
- DJANGO_SUPERUSER_PASSWORD - пароль для суперюзера
#### Установите Docker и Docker-compose:
- ```sudo apt install docker.io```
- ```sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o usr/local/bin/docker-compose```
- ```sudo chmod +x /usr/local/bin/docker-compose```
#### Выполнить команды для сбора статики;
- ```sudo docker-compose exec web python manage.py collectstatic --no-input```
#### создания и применения миграций;
- ```sudo docker-compose exec foodgram python manage.py makemigrations```
- ```sudo docker-compose exec foodgram python manage.py migrate --noinput```
#### для загрузки данных ингредиентов и тегов;
- ```sudo docker-compose exec foodgram python manage.py load_data```
#### создания суперюзера.
- ```sudo docker-compose exec foodgram python manage.py createsuperuser```
#### Для проверки:
 - ip сервера - 51.250.72.46
- Суперюзер: логин - admin, пароль - admin1234

