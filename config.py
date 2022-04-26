class Config(object):
    DEBUG = False
    TESTING = False


class ConfigDevelopment(Config):
    DEBUG = True


class ConfigTesting(Config):
    TESTING = True
