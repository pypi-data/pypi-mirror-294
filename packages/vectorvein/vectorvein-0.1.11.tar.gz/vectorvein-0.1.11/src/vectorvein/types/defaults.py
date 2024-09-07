# @Author: Bi Ying
# @Date:   2024-07-27 00:02:34
from .enums import ContextLengthControlType

CONTEXT_LENGTH_CONTROL = ContextLengthControlType.Latest

ENDPOINT_CONCURRENT_REQUESTS = 20
ENDPOINT_RPM = 60
ENDPOINT_TPM = 300000

MODEL_CONTEXT_LENGTH = 32768

# Moonshot models
MOONSHOT_MODELS = {
    "moonshot-v1-8k": {
        "id": "moonshot-v1-8k",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "moonshot-v1-32k": {
        "id": "moonshot-v1-32k",
        "context_length": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "moonshot-v1-128k": {
        "id": "moonshot-v1-128k",
        "context_length": 131072,
        "function_call_available": True,
        "response_format_available": True,
    },
}
MOONSHOT_DEFAULT_MODEL = "moonshot-v1-8k"

# Deepseek models
DEEPSEEK_MODELS = {
    "deepseek-chat": {
        "id": "deepseek-chat",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "deepseek-coder": {
        "id": "deepseek-chat",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
}
DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"

# Groq models
GROQ_DEFAULT_MODEL = "llama3-70b-8192"
GROQ_MODELS = {
    "mixtral-8x7b-32768": {
        "id": "mixtral-8x7b-32768",
        "context_length": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "llama3-70b-8192": {
        "id": "llama3-70b-8192",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "llama3-8b-8192": {
        "id": "llama3-8b-8192",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gemma-7b-it": {
        "id": "gemma-7b-it",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# Qwen models
QWEN_DEFAULT_MODEL = "qwen2-72b-instruct"
QWEN_MODELS = {
    "qwen1.5-1.8b-chat": {
        "id": "qwen1.5-1.8b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-4b-chat": {
        "id": "qwen1.5-4b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-7b-chat": {
        "id": "qwen1.5-7b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-14b-chat": {
        "id": "qwen1.5-14b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-32b-chat": {
        "id": "qwen1.5-32b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-72b-chat": {
        "id": "qwen1.5-72b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-110b-chat": {
        "id": "qwen1.5-110b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2-72b-instruct": {
        "id": "qwen2-72b-instruct",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
}

# Yi models
YI_DEFAULT_MODEL = "yi-large-turbo"
YI_MODELS = {
    "yi-large": {
        "id": "yi-large",
        "context_length": 32000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-large-turbo": {
        "id": "yi-large-turbo",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-large-fc": {
        "id": "yi-large-fc",
        "context_length": 32000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": False,
    },
    "yi-medium": {
        "id": "yi-medium",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-medium-200k": {
        "id": "yi-medium-200k",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-spark": {
        "id": "yi-spark",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-vision": {
        "id": "yi-vision",
        "context_length": 4000,
        "max_output_tokens": 2000,
        "function_call_available": False,
        "response_format_available": False,
    },
}

# ZhiPuAI models
ZHIPUAI_DEFAULT_MODEL = "glm-4-air"
ZHIPUAI_MODELS = {
    "glm-3-turbo": {
        "id": "glm-3-turbo",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4": {
        "id": "glm-4",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-plus": {
        "id": "glm-4-plus",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-0520": {
        "id": "glm-4-0520",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-air": {
        "id": "glm-4-air",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-airx": {
        "id": "glm-4-airx",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-flash": {
        "id": "glm-4-flash",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-long": {
        "id": "glm-4-long",
        "context_length": 1000000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4v": {
        "id": "glm-4v",
        "context_length": 2000,
        "function_call_available": False,
        "response_format_available": False,
        "max_output_tokens": 1024,
    },
    "glm-4v-plus": {
        "id": "glm-4v-plus",
        "context_length": 2000,
        "function_call_available": False,
        "response_format_available": False,
        "max_output_tokens": 1024,
    },
}

# Mistral models
MISTRAL_DEFAULT_MODEL = "mistral-small"
MISTRAL_MODELS = {
    "open-mistral-7b": {
        "id": "open-mistral-7b",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "open-mixtral-8x7b": {
        "id": "open-mixtral-8x7b",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "open-mixtral-8x22b": {
        "id": "open-mixtral-8x22b",
        "context_length": 64000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "open-mistral-nemo": {
        "id": "open-mistral-nemo",
        "context_length": 128000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "codestral-latest": {
        "id": "codestral-latest",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "mistral-small-latest": {
        "id": "mistral-small-latest",
        "context_length": 30000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "mistral-medium-latest": {
        "id": "mistral-medium-latest",
        "context_length": 30000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "mistral-large-latest": {
        "id": "mistral-large-latest",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# OpenAI models
OPENAI_DEFAULT_MODEL = "gpt-4o"
OPENAI_MODELS = {
    "gpt-35-turbo": {
        "id": "gpt-35-turbo",
        "context_length": 16385,
        "function_call_available": True,
        "response_format_available": True,
        "max_output_tokens": 4096,
    },
    "gpt-4-turbo": {
        "id": "gpt-4-turbo",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4": {
        "id": "gpt-4",
        "context_length": 8192,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4o": {
        "id": "gpt-4o",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4o-mini": {
        "id": "gpt-4o-mini",
        "context_length": 128000,
        "max_output_tokens": 16384,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4v": {
        "id": "gpt-4v",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# Anthropic models
ANTHROPIC_DEFAULT_MODEL = "claude-3-5-sonnet-20240620"
ANTHROPIC_MODELS = {
    "claude-3-opus-20240229": {
        "id": "claude-3-opus-20240229",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "claude-3-sonnet-20240229": {
        "id": "claude-3-sonnet-20240229",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "claude-3-haiku-20240307": {
        "id": "claude-3-haiku-20240307",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "claude-3-5-sonnet-20240620": {
        "id": "claude-3-5-sonnet-20240620",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# Minimax models
MINIMAX_DEFAULT_MODEL = "abab6.5s-chat"
MINIMAX_MODELS = {
    "abab5-chat": {
        "id": "abab5-chat",
        "context_length": 6144,
        "max_output_tokens": 6144,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab5.5-chat": {
        "id": "abab5.5-chat",
        "context_length": 16384,
        "max_output_tokens": 16384,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab6-chat": {
        "id": "abab6-chat",
        "context_length": 32768,
        "max_output_tokens": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab6.5s-chat": {
        "id": "abab6.5s-chat",
        "context_length": 245760,
        "max_output_tokens": 245760,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# Gemini models
GEMINI_DEFAULT_MODEL = "gemini-1.5-pro"
GEMINI_MODELS = {
    "gemini-1.5-pro": {
        "id": "gemini-1.5-pro",
        "context_length": 1048576,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gemini-1.5-flash": {
        "id": "gemini-1.5-flash",
        "context_length": 1048576,
        "function_call_available": True,
        "response_format_available": True,
    },
}
