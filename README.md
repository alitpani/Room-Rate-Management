# Django Project Setup

This document outlines the steps to set up a Django project with Docker and PostgreSQL, along with how to manage migrations, create a superuser, run the server, and run tests. Additionally, it covers how to access the Swagger documentation for the API.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Docker
- Docker Compose
- Git

## Setup Instructions

```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate

pip install -r requirements.txt

# Setup database:
cd Database && docker-compose up -d --build

# Create and Configure .env File

DOCKER_POSTGRES_DB=postgres
DOCKER_POSTGRES_USER=postgres
DOCKER_POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=4900
DEBUG=True
SECRET_KEY='django-insecure-**g25fs-4s-4fru8f#m6=&!miql0%#%2khohw(f80rw-awnbx9'

# Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

#  run server
python manage.py runserver
```

## Access swagger:

`http://127.0.0.1:8000/swagger/`

## Run tests:

`python manage.py test`
