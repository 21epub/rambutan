import os


class Config(object):
    DEBUG = True
    IMAGE_CONFIG = {
        "thumbnail_size": 400,
        "quality": 85,
    }

    SECRET_KEY = "dev"
    # STORAGE_PATH = "/path/to/images/"
    STORAGE_PATH = os.getenv("STORAGE_PATH", default="/tmp/images/")


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False

    STORAGE_PATH = os.getenv("STORAGE_PATH", default="/tmp/images/")


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
