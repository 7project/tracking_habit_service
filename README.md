# Как запустить tracking_habit_service
first create file `.env` to directory
to keys


```DB_HOST=your_host```

```DB_PORT=your_port```

```DB_NAME=your_name```

```DB_USER=your_user```

```DB_PASS=your_pass```

```DATABASE_URL=your_url```

```DATABASE_URL_NOT_ASYNC=driver postgresql your_url ```

```BOT_TOKEN="your_token_bot from @BotFather"```

```BLOCKED_ID_TELEGRAM_USER1=ID_USER```
```BLOCKED_ID_TELEGRAM_USER2=ID_USER```
```BLOCKED_ID_TELEGRAM_USER3=ID_USER```

to console install poetry

```pip install poetry```

```poetry config virtualenvs.create false```

install dependency project.toml

```poetry install --no-root --no-interaction --no-ansi```

two create folder name 
```/cert```

command shell

```openssl genrsa -out jwt-private.pem 2048```

```openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem```

in folder cert create to two file names:

```
jwt-private.pem  
jwt-public.pem
```

three, create migrations and first migrate database

```
docker-compose ps -a 
docker-compose exec -it fastapi alembic init -t async migrations
```
```
docker-compose exec -it fastapi alembic revision --autogenerate -m "create database"
docker-compose exec -it fastapi alembic upgrade head
```

docs [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration)

a folder named data and migrations will appear

before the first start there should be the following folders and files

```
data - postgreSQL
migrations - alembic
cert - openssl gen jwt-keys two files
.env - you person data
```

command start all project

```
docker-compose up
```
