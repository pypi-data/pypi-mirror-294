# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
from vectorvein.settings import settings
from vectorvein.chat_clients import (
    BackendType,
    get_token_counts,
)

from sample_settings import sample_settings


settings.load(sample_settings)


backend = BackendType.Moonshot
model = "moonshot-v1-8k"
backend = BackendType.OpenAI
model = "gpt-4o"
backend = BackendType.Anthropic
model = "claude-3-5-sonnet-20240620"
model = "claude-3-haiku-20240307"
model = "claude-3-opus-20240229"
# backend = BackendType.MiniMax
# model = "abab6.5s-chat"
# backend = BackendType.Gemini
# model = "gemini-1.5-flash"
# model = "gemini-1.5-pro"
# backend = BackendType.OpenAI
# model = "gpt-35-turbo"
# backend = BackendType.MiniMax
# model = "abab6.5s-chat"
# backend = BackendType.Yi
# model = "yi-large-fc"
# backend = BackendType.Mistral
# model = "mixtral-8x7b"
backend = BackendType.Qwen
model = "qwen2-72b-instruct"
# backend = BackendType.ZhiPuAI
# model = "glm-4-long"
# backend = BackendType.Moonshot
# model = "moonshot-v1-8k"
# backend = BackendType.DeepSeek
# model = "deepseek-chat"

tokens = get_token_counts("hello 我是毕老师", model)
print(tokens)
