class BaseStorage(object):

    def read(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def is_exist(self) -> bool:
        return True

    def save(self, dist):
        raise NotImplementedError()
