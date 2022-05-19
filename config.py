from common.environ import environ


class Config(object):
    DEBUG = False
    TESTING = False
    db_password = environ["DB_PASSWORD"]
    db_name = environ["DB_NAME"]

    @property
    def MONGO_URI(self):
        return f"mongodb+srv://krishna:{self.db_password}@cluster0.7oic7.mongodb.net/{self.db_name}?retryWrites=true&w=majority"


class ConfigProduction(Config):
    pass


class ConfigDevelopment(Config):
    DEBUG = True


class ConfigTesting(Config):
    TESTING = True
