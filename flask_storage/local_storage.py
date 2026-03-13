import os
from typing import Optional

from .base import BaseStorage


class FileStorage(BaseStorage):
    def get_abs_filename(self, filename: str) -> str:
        if self.storage_path.endswith("/"):
            _abs_filename = f"{self.storage_path}{filename}"
        else:
            _abs_filename = f"{self.storage_path}/{filename}"
        return _abs_filename

    def is_exist(self, filename: str) -> bool:
        return os.path.exists(self.get_abs_filename(filename))

    def delete(self, filename: str) -> Optional[bool]:
        return None

    def read(self, filename: str) -> bytes:
        with open(self.get_abs_filename(filename), mode="rb") as f:
            content = f.read()
        return content

    def save(self, filename: str, content: bytes) -> Optional[bool]:
        return None
