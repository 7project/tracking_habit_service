# Как запустить tracking_habit_service
# 1
```git clone https://github.com/7project/tracking_habit_service```

first, rename .env.template to file `.env` to base directory
Enter to keys:


```DB_HOST=your_host``` - deprecated 

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

# 2
```dcoker-compose up``` create containers 


## options

to console install poetry

```pip install poetry```

```poetry config virtualenvs.create false```

install dependency project.toml

```poetry install --no-root --no-interaction --no-ansi```

# 3

two create folder name at container fastapi

```docker exec -it fastapi bash```

```mkdir ./cert```

```chmod +x ./cert```

command shell

```cd ./cert```

```openssl genrsa -out jwt-private.pem 2048```

```openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem```

in folder cert create to two file names:

```
jwt-private.pem  
jwt-public.pem
```

# 4
## upgrade db

save dump

```docker exec -it postgres pg_dump -U <name_user> -d <name_db> -F c -b -v -f /var/lib/postgresql/data/backup_data.dump```

upload to local file system

```docker cp  postgres:/var/lib/postgresql/data/backup_data.dump ./backup_data.dump```

copy to server backend

```scp backup_data.dump <user_name>@<adress_ip>:/home/<name_user>/tracking_habit_service/```

copy to inner container folder tracking_habit_service

```docker cp ./backup_data.dump postgres:/var/lib/postgresql/data/backup_data.dump```

update database to container

```docker exec -i postgres pg_restore -U <name_user> -d <name_db> -v /var/lib/postgresql/data/backup_data.dump```

```docker-compose restart```

# options
## new database
### three, create migrations and first migrate database

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
