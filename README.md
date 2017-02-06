# ChatBy Server

## Setup

```bash
cd chatby-server
python3 -m venv chatby_env
source ./chatby_env/bin/activate
```

## Run

From the virtual environment:

```bash
cd chatby
python manage.py migrate
python manage.py runserver
```