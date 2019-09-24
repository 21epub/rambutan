class BaseStorage(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.storage_path = app.config.get("STORAGE_PATH", None)
        if self.storage_path is None:
            raise Exception("storage is None")

    def read(self, **kwargs):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def is_exist(self, **kwargs) -> bool:
        return True

    def save(self, dist):
        raise NotImplementedError()
