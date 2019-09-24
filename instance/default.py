class Config(object):
    DEBUG = True


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    # 'testing': TestingConfig,
    "production": ProductionConfig,
}
