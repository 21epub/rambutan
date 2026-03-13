import oss2

from .base import BaseStorage


class OssStorage(BaseStorage):
    """Aliyun OSS storage implementation."""

    def __init__(self, app=None):
        self.bucket = None
        self.bucket_name = None
        self.endpoint = None
        super().__init__(app)

    def init_app(self, app):
        super().init_app(app)

        # Get OSS configuration from app config
        self.bucket_name = app.config.get("OSS_BUCKET_NAME")
        self.endpoint = app.config.get("OSS_ENDPOINT")
        access_key_id = app.config.get("OSS_ACCESS_KEY_ID")
        access_key_secret = app.config.get("OSS_ACCESS_KEY_SECRET")

        if not all(
            [self.bucket_name, self.endpoint, access_key_id, access_key_secret]
        ):
            raise Exception(
                "OSS configuration is incomplete. Please check OSS_BUCKET_NAME, OSS_ENDPOINT, OSS_ACCESS_KEY_ID, and OSS_ACCESS_KEY_SECRET"
            )

        # Initialize OSS auth and bucket
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)

    def get_abs_filename(self, filename: str) -> str:
        """Get the full OSS object key."""
        if self.storage_path:
            if self.storage_path.endswith("/"):
                return "{}{}".format(self.storage_path, filename)
            return "{}/{}".format(self.storage_path, filename)
        return filename

    def is_exist(self, filename: str) -> bool:
        """Check if file exists in OSS."""
        key = self.get_abs_filename(filename)
        return self.bucket.object_exists(key)

    def delete(self, filename: str) -> bool:
        """Delete file from OSS."""
        key = self.get_abs_filename(filename)
        try:
            self.bucket.delete_object(key)
            return True
        except Exception:
            return False

    def read(self, filename: str) -> bytes:
        """Read file content from OSS."""
        key = self.get_abs_filename(filename)
        result = self.bucket.get_object(key)
        content = result.read()
        return content

    def save(self, filename: str, content: bytes) -> bool:
        """Save file to OSS."""
        key = self.get_abs_filename(filename)
        try:
            self.bucket.put_object(key, content)
            return True
        except Exception:
            return False
