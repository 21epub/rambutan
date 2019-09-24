from .base import BaseStorage
import os


class FileStorage(BaseStorage):

    def is_exist(self, filename) -> bool:
        abs_filename = self.storage_path + filename
        return os.path.exists(abs_filename)

    def delete(self):
        return

    def read(self, filename):

        abs_filename = self.storage_path + filename
        f = open(abs_filename, mode="rb")
        content = f.read()
        f.close()
        return content

    def save(self, dist):
        pass
