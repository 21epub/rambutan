import os
from .base import BaseStorage


class FileStorage(BaseStorage):
    def get_abs_filename(self, filename):
        if self.storage_path.endswith("/"):
            _abs_filename = f"{self.storage_path}{filename}"
        else:
            _abs_filename = f"{self.storage_path}/{filename}"
        return _abs_filename

    def is_exist(self, filename) -> bool:

        return os.path.exists(self.get_abs_filename(filename))

    def delete(self):
        return

    def read(self, filename):
        f = open(self.get_abs_filename(filename), mode="rb")
        content = f.read()
        f.close()
        return content

    def save(self, dist):
        pass
