import os
class BaseConfig():
   API_PREFIX = '/api'
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
   DEBUG = True
   BASE_DIR = os.path.abspath(os.path.dirname('..'))
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
   SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
   UPLOADED_FILES = os.path.join(BASE_DIR,'app/static')
   SECURITY_FRESHNESS_GRACE_PERIOD = 6000
   CACHE_TYPE = 'RedisCache'
   CACHE_REDIS_HOST = 'localhost'
   CACHE_REDIS_PORT = 6379
   BROKER_URL = 'redis://localhost:6379/01'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/02'
   
   JWT_SECRET_KEY = 't1MN89m4wnKj6nyJIUfmc2TpLJUI4nss'
   

class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   BASE_DIR = os.path.abspath(os.path.dirname(__file__))
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app_prod.db')
   SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
   
   
