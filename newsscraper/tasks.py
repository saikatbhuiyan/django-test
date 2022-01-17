from celery import shared_task
from currencyapi.celery  import app as celery_app
from .scrapers import scrape


URL = "https://dev.to/search?q=django"


@celery_app.task
def scrape_dev_to():
    scrape(URL)
    return


@shared_task  # allows us to call this function asynchronously
def scrape_async():
    scrape(URL)
    return

