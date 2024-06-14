from app.workers.workers import celery
from datetime import datetime


@celery.task()
def just_say_hello(name):
    print("Inside the task")
    print("Hello {}".format(name))