# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rambutan is a Flask-based image processing web service that provides image resizing and cropping functionality, similar to Qiniu Cloud's image processing API (Dora). It handles images with suffixes like `-thumb`, `-large`, `-hd` for different size variants.

## Development Commands

```bash
# Install dependencies
pip install -r requirement/dev.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting (black)
black .

# Run linting (flake8)
flake8 .

# Run tests
python -m pytest tests/

# Run a single test
python -m pytest tests/test_crop.py -v

# Run the Flask app locally
FLASK_APP=apps flask run
# Or
python -c "from apps import create_app; app = create_app(); app.run()"
```

## Architecture

### Application Structure
- `apps/` - Main Flask application
  - `views/images/` - Image processing views and business logic
    - `views.py` - ResizeImageView endpoint (`/epub360-media/<regex:filename>`)
    - `mixins.py` - ProcessImageMixin with resize and crop logic
    - `handles/jpg_handle.py` - ImageProcessor class for actual image operations
- `flask_storage/` - Storage abstraction layer
  - `base.py` - BaseStorage abstract class
  - `local_storage.py` - FileStorage implementation for local filesystem
  - `remote_storage.py` - Remote storage support (not implemented)
- `instance/config.py` - Configuration for development/testing/production

### Image Processing Flow
1. Request comes to `/epub360-media/<filename>` with optional size suffix (`-thumb`, `-large`, `-hd`)
2. `ResizeImageView` extracts filename and size from URL
3. Storage layer reads the original image file
4. `ProcessImageMixin.resize()` or `crop_with_param()` processes the image using `ImageProcessor`
5. Processed image is returned as response with appropriate MIME type

### Configuration
- `STORAGE_PATH` - Path where images are stored (default: `/tmp/images/`)
- `IMAGE_CONFIG` - Image processing settings:
  - `thumbnail_size` - Default thumbnail size (320px)
  - `quality` - JPEG quality (90)
- `SECRET_KEY` - Flask secret key

## Key Implementation Details

### Crop Parameter Format
The crop functionality uses Qiniu-style parameters:
- `/crop/<Width>x<Height>` - Specify both dimensions
- `/crop/<Width>x` - Width only, height auto
- `/crop/x<Height>` - Height only, width auto
- `/crop/!{size}a<dx>a<dy>` - With offset

### EXIF Handling
Images are processed with `ImageOps.exif_transpose()` to fix rotation issues caused by EXIF orientation data.

### Storage Abstraction
The storage layer can be extended to support remote storage (S3, OSS, etc.) by implementing `BaseStorage`.
