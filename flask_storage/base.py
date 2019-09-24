class BaseStorage(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def read(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def is_exist(self) -> bool:
        return True

    def save(self, dist):
        raise NotImplementedError()
