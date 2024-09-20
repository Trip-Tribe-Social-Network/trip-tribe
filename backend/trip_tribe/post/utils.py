from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(image, max_size_kb=150):
    max_size_bytes = max_size_kb * 1024  # Convert KB to bytes
    img = Image.open(image)
    
    # Resize the image to a smaller dimension before compression
    width, height = img.size
    img.thumbnail((width // 2, height // 2))

    # Compress the image
    quality = 85  # Initial quality
    buffer = BytesIO()
    img.save(buffer, format='JPEG', optimize=True, quality=quality)
    
    while buffer.tell() > max_size_bytes and quality > 10:
        buffer = BytesIO()
        quality -= 5  # Decrease quality to further compress
        img.save(buffer, format='JPEG', optimize=True, quality=quality)

    # If the image is still too large, resize it further
    if buffer.tell() > max_size_bytes:
        width, height = img.size
        img.thumbnail((width // 2, height // 2))
        buffer = BytesIO()
        img.save(buffer, format='JPEG', optimize=True, quality=quality)

    return ContentFile(buffer.getvalue(), name=image.name)