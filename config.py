import os


class Config(object):
    TESTING = False
    DB_SERVER = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{self.DB_SERVER}/{os.environ.get('DB_NAME')}"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    pass


class TestingConfig(object):
    DB_SERVER = 'localhost'
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'sqlite:///:memory:'
