from PIL import Image
import os

def compress_image(image_path, max_size_mb=1):
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    with Image.open(image_path) as img:
        # Check if the image size is already less than the max size
        if os.path.getsize(image_path) <= max_size_bytes:
            return

        # Compress the image
        quality = 85  # Initial quality
        while os.path.getsize(image_path) > max_size_bytes and quality > 10:
            img.save(image_path, optimize=True, quality=quality)
            quality -= 5  # Decrease quality to further compress

        # If the image is still too large, resize it
        if os.path.getsize(image_path) > max_size_bytes:
            width, height = img.size
            img.thumbnail((width // 2, height // 2))
            img.save(image_path, optimize=True, quality=quality)