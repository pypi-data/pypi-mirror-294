# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
from .base_client import BaseChatClient, BaseAsyncChatClient

from .yi_client import YiChatClient, AsyncYiChatClient
from .groq_client import GroqChatClient, AsyncGroqChatClient
from .qwen_client import QwenChatClient, AsyncQwenChatClient
from .local_client import LocalChatClient, AsyncLocalChatClient
from .gemini_client import GeminiChatClient, AsyncGeminiChatClient
from .openai_client import OpenAIChatClient, AsyncOpenAIChatClient
from .zhipuai_client import ZhiPuAIChatClient, AsyncZhiPuAIChatClient
from .minimax_client import MiniMaxChatClient, AsyncMiniMaxChatClient
from .mistral_client import MistralChatClient, AsyncMistralChatClient
from .moonshot_client import MoonshotChatClient, AsyncMoonshotChatClient
from .deepseek_client import DeepSeekChatClient, AsyncDeepSeekChatClient

from ..types import defaults as defs
from ..types.enums import BackendType, ContextLengthControlType
from .anthropic_client import AnthropicChatClient, AsyncAnthropicChatClient
from .utils import format_messages, get_token_counts, ToolCallContentProcessor


BackendMap = {
    "sync": {
        BackendType.Anthropic: AnthropicChatClient,
        BackendType.DeepSeek: DeepSeekChatClient,
        BackendType.Gemini: GeminiChatClient,
        BackendType.Groq: GroqChatClient,
        BackendType.Local: LocalChatClient,
        BackendType.MiniMax: MiniMaxChatClient,
        BackendType.Mistral: MistralChatClient,
        BackendType.Moonshot: MoonshotChatClient,
        BackendType.OpenAI: OpenAIChatClient,
        BackendType.Qwen: QwenChatClient,
        BackendType.Yi: YiChatClient,
        BackendType.ZhiPuAI: ZhiPuAIChatClient,
    },
    "async": {
        BackendType.Anthropic: AsyncAnthropicChatClient,
        BackendType.DeepSeek: AsyncDeepSeekChatClient,
        BackendType.Gemini: AsyncGeminiChatClient,
        BackendType.Groq: AsyncGroqChatClient,
        BackendType.Local: AsyncLocalChatClient,
        BackendType.MiniMax: AsyncMiniMaxChatClient,
        BackendType.Mistral: AsyncMistralChatClient,
        BackendType.Moonshot: AsyncMoonshotChatClient,
        BackendType.OpenAI: AsyncOpenAIChatClient,
        BackendType.Qwen: AsyncQwenChatClient,
        BackendType.Yi: AsyncYiChatClient,
        BackendType.ZhiPuAI: AsyncZhiPuAIChatClient,
    },
}


def create_chat_client(
    backend: BackendType,
    model: str | None = None,
    stream: bool = False,
    temperature: float = 0.7,
    context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
    **kwargs,
) -> BaseChatClient:
    if backend.lower() not in BackendMap["sync"]:
        raise ValueError(f"Unsupported backend: {backend}")
    else:
        backend_key = backend.lower()

    ClientClass = BackendMap["sync"][backend_key]
    if model is None:
        model = ClientClass.DEFAULT_MODEL
    return BackendMap["sync"][backend_key](
        model=model,
        stream=stream,
        temperature=temperature,
        context_length_control=context_length_control,
        **kwargs,
    )


def create_async_chat_client(
    backend: BackendType,
    model: str | None = None,
    stream: bool = False,
    temperature: float = 0.7,
    context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
    **kwargs,
) -> BaseAsyncChatClient:
    if backend.lower() not in BackendMap["async"]:
        raise ValueError(f"Unsupported backend: {backend}")
    else:
        backend_key = backend.lower()

    ClientClass = BackendMap["async"][backend_key]
    if model is None:
        model = ClientClass.DEFAULT_MODEL
    return BackendMap["async"][backend_key](
        model=model,
        stream=stream,
        temperature=temperature,
        context_length_control=context_length_control,
        **kwargs,
    )


__all__ = [
    "BackendType",
    "format_messages",
    "get_token_counts",
    "create_chat_client",
    "create_async_chat_client",
    "ToolCallContentProcessor",
]
