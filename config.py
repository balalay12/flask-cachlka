import os


class Config(object):

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super-puper-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    DEBUG = True


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
