# en-mi-club-backend

Python 3.12

## Instructions to run with docker

First, create a `.env` file at the root of the project with the `.env.example` variables.

Then, run:

```bash
docker compose build
```

```bash
docker compose up
```

Migrations are run automatically when you run the `docker compose up` command, but you have to create them first.

## Instructions to run black and ruff

Just run

```bash
black -l 80 src/
```

```bash
ruff check --fix src/
```

## Connect to web container to make migrations

Connect to web container

```bash
docker-compose exec web /bin/sh
```

make migration

```bash
alembic revision --autogenerate -m "message"
```

## Create venv

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```