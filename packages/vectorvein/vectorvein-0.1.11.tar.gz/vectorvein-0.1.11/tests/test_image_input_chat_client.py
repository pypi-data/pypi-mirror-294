# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
import time
from pathlib import Path

from vectorvein.settings import settings
from vectorvein.chat_clients import create_chat_client
from vectorvein.utilities.media_processing import ImageProcessor

from sample_settings import sample_settings

settings.load(sample_settings)
image = Path("./cat.png")
image_processor = ImageProcessor(image)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "描述这张图片。"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_processor.mime_type,
                    "data": image_processor.base64_image,
                },
            },
        ],
    }
]


backend = "zhipuai"
model = "glm-4v"
backend = "openai"
model = "gpt-4o"
backend = "anthropic"
model = "claude-3-5-sonnet-20240620"
start_time = time.perf_counter()
client = create_chat_client(backend, model=model, stream=False)
response = client.create_completion(messages=messages)
print(response)
end_time = time.perf_counter()
print(f"Stream time elapsed: {end_time - start_time} seconds")
