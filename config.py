import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    ENV = "development"
    SECRET_KEY = "9as8df(*S*8(das0ˆSˆD%5a67900SA(D*00"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
