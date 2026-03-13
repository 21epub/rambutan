import os


class Config(object):
    DEBUG = True
    IMAGE_CONFIG = {
        "thumbnail_size": 320,
        "quality": 90,
    }

    SECRET_KEY = "dev"
    STORAGE_PATH = os.getenv("STORAGE_PATH", default="/tmp/images/")

    # Storage type: 'local' or 'oss'
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", default="local")

    # Aliyun OSS configuration (used when STORAGE_TYPE is 'oss')
    OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME", default="")
    OSS_ENDPOINT = os.getenv("OSS_ENDPOINT", default="")
    OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID", default="")
    OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET", default="")


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False

    # STORAGE_PATH = os.getenv("STORAGE_PATH", default="/tmp/images/")


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
