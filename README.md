# ChatBy Server

## Setup virtual environment

After cloning the repo:

```bash
cd chatby-server
python3 -m venv env
source ./env/bin/activate
```

## Install dependencies

From the virtual environment:

```bash
pip install -r requirements.txt
```

## Run

From the virtual environment:

```bash
python manage.py migrate
python manage.py runserver
```
