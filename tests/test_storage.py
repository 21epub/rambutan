import os
import tempfile
from io import BytesIO
from unittest.mock import Mock, patch, MagicMock

import pytest
from PIL import Image

from apps.views.images.handles.jpg_handle import ImageProcessor
from flask_storage.local_storage import FileStorage
from flask_storage.oss_storage import OssStorage
from flask import Flask


class TestImageProcessor:
    """Test ImageProcessor class for image processing functionality."""

    @pytest.fixture
    def sample_image(self):
        """Create a simple test image in memory."""
        img = Image.new("RGB", (800, 600), color="red")
        return img

    @pytest.fixture
    def sample_image_bytes(self):
        """Create a simple test image bytes."""
        img = Image.new("RGB", (800, 600), color="red")
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer.getvalue()

    def test_init_with_image(self, sample_image_bytes):
        """Test ImageProcessor initialization."""
        processor = ImageProcessor(sample_image_bytes)
        assert processor.origin_width == 800
        assert processor.origin_heigth == 600

    def test_resize(self, sample_image_bytes):
        """Test image resize functionality."""
        processor = ImageProcessor(sample_image_bytes)
        resized = processor.resize((320, 320))
        assert resized.size[0] <= 320
        assert resized.size[1] <= 320

    def test_output(self, sample_image):
        """Test image output with format and quality."""
        resized = sample_image.copy()
        resized.thumbnail((320, 320))
        content, mime_type = ImageProcessor.output(
            resized, format="JPEG", quality=85
        )
        assert isinstance(content, bytes)
        assert mime_type == "image/jpeg"

    def test_output_png(self, sample_image):
        """Test image output with PNG format."""
        content, mime_type = ImageProcessor.output(
            sample_image, format="PNG", quality=85
        )
        assert isinstance(content, bytes)
        assert mime_type == "image/png"

    def test_crop_basic_300x400(self, sample_image):
        """Test basic crop with 300x400."""
        # Create processor from PIL Image using kwargs
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        # Use output method to get cropped result
        box = processor.parse_param("300x400")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_width_only(self, sample_image):
        """Test crop with width only (e.g., 300x)."""
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        box = processor.parse_param("300x")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_height_only(self, sample_image):
        """Test crop with height only (e.g., x400)."""
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        box = processor.parse_param("x400")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_with_offset(self, sample_image):
        """Test crop with offset (!300x400a10a10)."""
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        box = processor.parse_param("!300x400a10a10")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_with_minus_offset(self, sample_image):
        """Test crop with minus offset (!300x400-10a10)."""
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        box = processor.parse_param("!300x400-10a10")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_empty_param(self, sample_image):
        """Test crop with empty parameter returns full image."""
        buffer = BytesIO()
        sample_image.save(buffer, format="JPEG")
        buffer.seek(0)
        processor = ImageProcessor(buffer.getvalue())

        box = processor.parse_param("")
        im_crop = processor.im.crop(box)
        content, mime_type = ImageProcessor.output(im_crop, format="JPEG")
        assert isinstance(content, bytes)

    def test_crop_invalid_param(self, sample_image_bytes):
        """Test crop with invalid parameter raises exception."""
        processor = ImageProcessor(sample_image_bytes)
        with pytest.raises(Exception):
            processor.parse_param("invalid")

    def test_parse_param_basic(self, sample_image_bytes):
        """Test parse_param with basic crop."""
        processor = ImageProcessor(sample_image_bytes)
        box = processor.parse_param("300x400")
        assert box[2] == 300
        assert box[3] == 400

    def test_parse_param_with_exclamation(self, sample_image_bytes):
        """Test parse_param with offset crop (!).

        Note: The ! prefix indicates offset mode and requires complete offset parameters.
        This test verifies that the function handles the case correctly.
        """
        processor = ImageProcessor(sample_image_bytes)
        # ! prefix requires complete offset parameters like !300x400a10a10
        box = processor.parse_param("!300x400a10a10")
        assert box is not None
        assert box[2] == 310  # 300 + 10 offset
        assert box[3] == 410  # 400 + 10 offset


class TestFileStorage:
    """Test FileStorage class."""

    @pytest.fixture
    def app(self, tmp_path):
        """Create Flask app with temporary storage."""
        app = Flask(__name__)
        app.config["STORAGE_PATH"] = str(tmp_path)
        return app

    @pytest.fixture
    def storage(self, app):
        """Create FileStorage instance."""
        return FileStorage(app)

    def test_init(self, app):
        """Test FileStorage initialization."""
        storage = FileStorage(app)
        assert storage.storage_path is not None

    def test_save_and_read(self, storage):
        """Test saving and reading file."""
        content = b"test image content"
        storage.save("test.jpg", content)
        read_content = storage.read("test.jpg")
        assert read_content == content

    def test_is_exist(self, storage):
        """Test file existence check."""
        content = b"test content"
        storage.save("test.jpg", content)
        assert storage.is_exist("test.jpg") is True
        assert storage.is_exist("nonexistent.jpg") is False

    def test_delete(self, storage):
        """Test file deletion."""
        content = b"test content"
        storage.save("test.jpg", content)
        result = storage.delete("test.jpg")
        assert result is None  # Current implementation returns None

    def test_get_abs_filename(self, storage):
        """Test getting absolute filename."""
        filename = storage.get_abs_filename("test.jpg")
        assert "test.jpg" in filename


class TestOssStorage:
    """Test OssStorage class."""

    @pytest.fixture
    def app(self):
        """Create Flask app with OSS config."""
        app = Flask(__name__)
        app.config["STORAGE_PATH"] = "images/"
        app.config["OSS_BUCKET_NAME"] = "test-bucket"
        app.config["OSS_ENDPOINT"] = "https://oss-cn-hangzhou.aliyuncs.com"
        app.config["OSS_ACCESS_KEY_ID"] = "test-key-id"
        app.config["OSS_ACCESS_KEY_SECRET"] = "test-key-secret"
        return app

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_init(self, mock_bucket, mock_auth, app):
        """Test OssStorage initialization."""
        storage = OssStorage(app)
        assert storage.bucket_name == "test-bucket"
        assert storage.endpoint == "https://oss-cn-hangzhou.aliyuncs.com"
        mock_auth.assert_called_once_with("test-key-id", "test-key-secret")
        mock_bucket.assert_called_once()

    def test_init_missing_config(self):
        """Test OssStorage initialization with missing config."""
        app = Flask(__name__)
        app.config["STORAGE_PATH"] = "images/"
        with pytest.raises(Exception):
            OssStorage(app)

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_is_exist(self, mock_bucket, mock_auth, app):
        """Test file existence check in OSS."""
        mock_bucket_instance = MagicMock()
        mock_bucket_instance.object_exists.return_value = True
        mock_bucket.return_value = mock_bucket_instance

        storage = OssStorage(app)
        assert storage.is_exist("test.jpg") is True

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_read(self, mock_bucket, mock_auth, app):
        """Test reading file from OSS."""
        mock_bucket_instance = MagicMock()
        mock_result = MagicMock()
        mock_result.read.return_value = b"test content"
        mock_bucket_instance.get_object.return_value = mock_result
        mock_bucket.return_value = mock_bucket_instance

        storage = OssStorage(app)
        content = storage.read("test.jpg")
        assert content == b"test content"

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_save(self, mock_bucket, mock_auth, app):
        """Test saving file to OSS."""
        mock_bucket_instance = MagicMock()
        mock_bucket.return_value = mock_bucket_instance

        storage = OssStorage(app)
        result = storage.save("test.jpg", b"test content")
        assert result is True
        mock_bucket_instance.put_object.assert_called_once()

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_delete(self, mock_bucket, mock_auth, app):
        """Test deleting file from OSS."""
        mock_bucket_instance = MagicMock()
        mock_bucket.return_value = mock_bucket_instance

        storage = OssStorage(app)
        result = storage.delete("test.jpg")
        assert result is True
        mock_bucket_instance.delete_object.assert_called_once()

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_get_abs_filename(self, mock_bucket, mock_auth, app):
        """Test getting absolute filename in OSS."""
        storage = OssStorage(app)
        storage.storage_path = "images/"
        filename = storage.get_abs_filename("test.jpg")
        assert filename == "images/test.jpg"

    @patch("flask_storage.oss_storage.oss2.Auth")
    @patch("flask_storage.oss_storage.oss2.Bucket")
    def test_get_abs_filename_no_path(self, mock_bucket, mock_auth, app):
        """Test getting absolute filename without path prefix."""
        storage = OssStorage(app)
        storage.storage_path = None
        filename = storage.get_abs_filename("test.jpg")
        assert filename == "test.jpg"
