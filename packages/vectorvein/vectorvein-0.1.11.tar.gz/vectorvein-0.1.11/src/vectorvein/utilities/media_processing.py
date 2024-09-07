# @Author: Bi Ying
# @Date:   2024-07-27 12:03:49
import base64
from io import BytesIO
from pathlib import Path
from functools import cached_property

import httpx
from PIL import Image



class ImageProcessor:
    def __init__(self, image_source: Image.Image | str | Path, max_size: int | None = 5 * 1024 * 1024):
        self.image_source = image_source
        if isinstance(image_source, (Image.Image, Path)):
            self.is_local = True
        else:
            self.is_local = not image_source.startswith("http")
        self.max_size = max_size
        self._image = self._load_image()

    def _load_image(self):
        if not self.is_local:
            image_url = self.image_source
            response = httpx.get(image_url)
            return Image.open(BytesIO(response.content))
        else:
            return Image.open(self.image_source)

    def _resize_image(self, img, max_size):
        img_bytes = BytesIO()
        img.save(img_bytes, format=img.format, optimize=True)

        if img_bytes.getbuffer().nbytes <= max_size:
            return img_bytes

        original_size = img.size
        scale_factor = 0.9

        while True:
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            img_bytes_resized = BytesIO()
            img_resized.save(img_bytes_resized, format=img.format, optimize=True)

            if img_bytes_resized.getbuffer().nbytes <= max_size:
                return img_bytes_resized

            scale_factor -= 0.1
            if scale_factor < 0.1:
                return img_bytes_resized

    @cached_property
    def base64_image(self):
        if self.max_size is None:
            return base64.b64encode(self._image.getvalue()).decode()

        img_bytes_resized = self._resize_image(self._image, self.max_size)
        return base64.b64encode(img_bytes_resized.getvalue()).decode()

    @cached_property
    def mime_type(self):
        return Image.MIME[self._image.format]

    @cached_property
    def data_url(self):
        return f"data:{self.mime_type};base64,{self.base64_image}"

