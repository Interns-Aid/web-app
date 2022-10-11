import os
from datetime import timedelta


class Config(object):
    TESTING = False
    DB_SERVER = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['headers']

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{self.DB_SERVER}/{os.environ.get('DB_NAME')}"

    @property
    def JWT_SECRET_KEY(self):
        return os.environ.get('JWT_SECRET_KEY')

    @property
    def SECRET_KEY(self):
        return os.environ.get('SECRET_KEY')

    @property
    def JWT_ACCESS_TOKEN_EXPIRES(self):
        return timedelta(hours=1)

    @property
    def JWT_REFRESH_TOKEN_EXPIRES(self):
        return timedelta(days=30)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'


class TestingConfig(Config):
    DB_SERVER = 'localhost'
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'sqlite:///:memory:'
