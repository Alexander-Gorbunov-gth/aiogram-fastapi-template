# Шаблон сервера для Телеграм бота. 

## Функционал
* Готов к запуску на VDS и открыт для расширения микросервисами (docker-compose)
* Бот на aiogram | aiogram_dialog
* Webhook с помощmю fastapi, при развороте локально, используйте например [вот этот тунель](https://play.devhook.ru/)
* База данных - PostgreSQL, доступ через SQLModel
* Настроена админка для работы с БД
* NoSQL - Redis


## Админка

### Доступ к админке
```/admin```

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

### При запуске docker-compose.yml - копируем статику для админки
```
  sudo docker compose -f docker-compose.yml exec tg_bot mkdir /app/static/admin/

  sudo docker compose -f docker-compose.yml exec tg_bot cp -r /app/tmp_file/admin_statics/. /app/static/admin/statics/ 
```

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

## Создать Superuser для доступа к админке

### 1. В переменных окржуения .env установите 
  ```
  debug = True
  superuser_key = <your_secret_key>
  ```
### 2. В схеме OpenApi используйте метод /create-superuser/

Генерация Secret key

openssl rand -hex 32


