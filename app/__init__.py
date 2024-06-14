

from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, current_app
from flask_login import LoginManager, current_user
from flask_cors import CORS
from flask_admin import Admin
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from app.workers import workers
from celery import Celery

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
admin = Admin(name='Dashboard')
migrate = Migrate()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
bootstrap = Bootstrap()
moment = Moment()
jwt = JWTManager()
cache = Cache()
celery = None

def create_app():
    
    app = Flask(__name__, static_folder='static')
    app.config.from_object('app.config')
    # initialize SQLAlchemy
    db.init_app(app)
    
    
    migrate.init_app(app, db, render_as_batch=True)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    api.init_app(app)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    #app.app_context().push()

    # define hello world page
    CORS(app)
    """ celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask """
    """ app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://127.0.0.1:6379/01",
        result_backend="redis://127.0.0.1:6379/02",
        task_ignore_result=True,
        ),
    )
    celery_app = workers.celery_init_app(app) """
    """ celery = Celery(app.name, broker_url=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config) """

    celery = workers.make_celery(app)

   

    return app

from app import models
from app.api import api

