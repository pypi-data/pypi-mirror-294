# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
import time
from pathlib import Path

from vectorvein.settings import settings
from vectorvein.chat_clients import create_chat_client
from vectorvein.chat_clients.utils import format_messages

from sample_settings import sample_settings

settings.load(sample_settings)
image = Path("./cat.png")

vectorvein_messages = [
    {
        "author_type": "U",
        "content_type": "TXT",
        "content": {
            "text": "描述这张图片。",
        },
        "attachments": [str(image)],
    }
]


backend = "moonshot"
model = "moonshot-v1-8k"
backend = "openai"
model = "gpt-4o"
backend = "anthropic"
model = "claude-3-5-sonnet-20240620"

messages = format_messages(vectorvein_messages, backend=backend, native_multimodal=True)

start_time = time.perf_counter()
client = create_chat_client(backend, model=model, stream=False)
response = client.create_completion(messages=messages)
print(response)
end_time = time.perf_counter()
print(f"Stream time elapsed: {end_time - start_time} seconds")
