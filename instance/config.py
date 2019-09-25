class Config(object):
    DEBUG = True
    IMAGE_CONFIG = {
        "thumbnail_size": 400,
        "quality": 85,
    }

    SECRET_KEY = "dev"
    STORAGE_PATH = "/path/to/image/"


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    'testing': TestingConfig,
    "production": ProductionConfig,
}
