import base64
from io import BytesIO
from PIL import Image, ImageSequence

from family_organizer import settings


def make_thumbnail_base64_str(image_path: str, max_size: int = settings.IMAGE_MIN_SIZE) -> str:
    """Returns string of encoded image by path, resizing it to acceptable size with ratio saved"""
    image_buffer = BytesIO()
    image = Image.open(settings.FILE_STORAGE + image_path)
    image.thumbnail((max_size, max_size))
    image.convert('RGB').save(image_buffer, format='JPEG')
    image_bytes = image_buffer.getvalue()
    image_encoded = base64.b64encode(image_bytes).decode('utf8')
    # if settings.DEBUG:
    #     print(image_encoded)
    return image_encoded
