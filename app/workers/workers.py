from celery import Celery, Task
from flask import current_app as app

""" celery = Celery("Application Jobs")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs) """

""" def celery_init_app(app: app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app """

from flask import Flask
#from celery import Celery

def make_celery(app=None):
    app = app 
    celery = Celery(
        app.import_name,
        backend="redis://localhost:6379/0",
        broker="redis://localhost:6379/1"
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery