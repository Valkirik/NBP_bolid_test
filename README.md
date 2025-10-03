# NBP_bolid_test

## Запуск проекта
### 1. Клонирование репозитория
- git clone https://github.com/Valkirik/NBP_bolid_test
- cd NBP_bolid_test

### 2. Создать файд ".env" в корне проекта
- touch .env
```env
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль
```

### 3. Запуск Docker
- docker compose build
- docker compose up -d

### 4. Создание супер-пользователя
- docker compose exec web python manage.py createsuperuser