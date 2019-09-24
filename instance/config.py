class Config(object):
    DEBUG = True
    IMAGE_CONFIG = {
        "thumbnail_size": 400,
        "quality": 85,
    }

    STORAGE_PATH = "/Users/xiejiaxin/Desktop/"


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    # 'testing': TestingConfig,
    "production": ProductionConfig,
}
