# Django News Scraper

This is a Django project with a dashboard of news scraped using Celery Tasks

## Project setup

1. Python version management with pyenv
   (pip install pipenv)
2. Virtual environments with pipenv
   (pipenv install)
3. Active environment
   (pipenv shell)

## Getting started

To activate this project's virtualenv, run `pipenv shell`.

You will need to copy the `.env.example` file and rename it `.env`. Inside there you can fill in the values of the environment variables, create a database and you're all good to go.

## Show Celery Task Using `django_celery_beat`

- celery -A newsscraper worker -l INFO
- celery -A newsscraper beat -l INFO

## Show Celery Task Using `flower`

Launch the Flower server at specified port other than default 5555 (open the UI at <http://localhost:5566>):

- celery flower --port=5566

Specify Celery application path with address and port for Flower:

- celery -A newsscraper flower --address=127.0.0.6 --port=5566

Launch using docker:

- docker run -p 5555:5555 mher/flower

Launch with unix socket file:

- celery flower --unix-socket=/tmp/flower.sock

Broker URL and other configuration options can be passed through the standard Celery options (notice that they are after Celery command and before Flower sub-command):
-celery --broker=amqp://guest:guest@localhost:5672// flower

## Rename your project

Rename your project with python manage.py rename <yourprojectname> <newprojectname>
