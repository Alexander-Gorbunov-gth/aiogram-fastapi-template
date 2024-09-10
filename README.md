# Шаблон сервера для Телеграм бота. 
Готовый шаблон для запуска микросервиса бота в ТГ

## Стэк:
* aiogram | aiogram_dialog
* FastApi
* SQLModel
* PostgreSQL
* Redis
* JWT
* Docker
* Uvicorn
* Nginx

## Функционал
* Готов к запуску на VDS и открыт для расширения микросервисами (docker-compose)
* Бот на aiogram | aiogram_dialog
* Webhook с помощmю fastapi, при развороте локально, используйте например [вот этот тунель](https://play.devhook.ru/)
* База данных - PostgreSQL, доступ через SQLModel
* Настроена админка для работы с БД
* NoSQL - Redis
* Проект разбит на прилодения в папке /apps
* Пример в папке /apps/core_app

## Запуск локально
* Клонируйте репозиторий и активируйте виртуальное окружение
* Установите и запустите Docker
* Переименуйте .env.example в .env и внесите свои данные
* Для base_webhook_url испольщуйте например [вот этот тунель](https://play.devhook.ru/) на порт - 80
* Выполните из дериктории проекта (запустит docker compose)
```
  make run 
```
* Примените миграции 
```
  sudo docker compose -f docker-compose.yml exec tg_bot alembic upgrade head

```
* Скопируйте статику для админки
```
  sudo docker compose -f docker-compose.yml exec tg_bot mkdir /app/static/admin/

  sudo docker compose -f docker-compose.yml exec tg_bot cp -r /app/tmp_file/admin_statics/. /app/static/admin/statics/ 

```
* Зайди в документацию и создайте Superuser (инструкция ниже)
```
  localhost/api/docs
```
* Админка доступна по адресу
```
  localhost/bot/admin
```


## Создать Superuser для доступа к админке

### 1. В переменных окржуения .env установите 
  ```
  debug = True
  superuser_key = <your_secret_key>
  ```
### 2. В схеме OpenApi используйте метод /create-superuser/
```
  localhost/api/docs
```


## Админка

### Доступ к админке
```localhost/bot/admin```

### Для регистрации модели (table=True) испольщуем @admin_site.reg из core.admin
```
    # apps/<название вашего модуля>/admin.py
    from sqladmin import ModelView

    from .models.user import FastApiUser
    from core.admin import admin_site


    @admin_site.reg
    class UserAdmin(ModelView, model=FastApiUser):
        column_list = [FastApiUser.id, FastApiUser.name]

```
### [Документация для админки](https://aminalaee.dev/sqladmin/configurations/)


## Alembic 

### 1. Создать миграции 
 ```
 alembic revision --autogenerate -m "init"
 ```

### 2. Применить миграции
  ```
  alembic upgrade head
  ```

__Примечание__
> Для Alembic при создании миграций будут автоматически импортированы файлы с моделями SQLModel из папок apps/<название вашего модуля>/models/



## Для генерации Secret key
```
  openssl rand -hex 32
 ```

## Для разработки проекта

* Из директории tg_bot устанавливаем зависимости
* Запускаем локально сервер PostgreSQL и Redis
* .dev.env.example переименовывем в .dev.env и вносим свои данные
* Запускаем FastAPI + aiogram через Uvicorn в режиме перезагрузки (на порт - 8000)
```
  make run
```

## Примечание

В проект добавлял идеи, взятые из Django, которых не хватало в FastApi (например админка и автоматическая регистрация моделей для миграции).
Со временем в папку /utils буду вносить доп функции для ускорения работы в проекте.