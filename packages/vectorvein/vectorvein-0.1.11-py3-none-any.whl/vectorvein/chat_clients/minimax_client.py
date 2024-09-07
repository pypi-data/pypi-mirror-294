# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
import json
import random

import httpx
from openai._types import NotGiven

from ..settings import settings
from ..types import defaults as defs
from .utils import cutoff_messages, get_token_counts
from .base_client import BaseChatClient, BaseAsyncChatClient
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import ChatCompletionMessage, ChatCompletionDeltaMessage


def extract_tool_calls(response):
    try:
        message = response["choices"][0].get("delta") or response["choices"][0].get("message", {})
        tool_calls = message.get("tool_calls")
        if tool_calls:
            return {
                "tool_calls": [
                    {
                        "index": index,
                        "id": tool_call["id"],
                        "function": tool_call["function"],
                        "type": "function",
                    }
                    for index, tool_call in enumerate(tool_calls)
                ]
            }
        else:
            return {}
    except Exception:
        return {}


class MiniMaxChatClient(BaseChatClient):
    DEFAULT_MODEL: str = defs.MINIMAX_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.MiniMax

    def __init__(
        self,
        model: str = defs.MINIMAX_DEFAULT_MODEL,
        stream: bool = True,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        **kwargs,
    ):
        super().__init__(
            model,
            stream,
            temperature,
            context_length_control,
            random_endpoint,
            endpoint_id,
            **kwargs,
        )
        self.http_client = httpx.Client()

    def create_completion(
        self,
        messages: list = list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: list | None = None,
        tool_choice: str = "auto",
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature
        if isinstance(tool_choice, NotGiven):
            tool_choice = "auto"

        self.model_setting = self.backend_settings.models[self.model]
        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            tools_params = {
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": tool["function"]["name"],
                            "description": tool["function"].get("description", ""),
                            "parameters": json.dumps(
                                tool["function"].get("parameters", {})
                            ),  # 非要搞不同，parameters 是个字符串
                        },
                    }
                    for tool in tools
                ],
                "tool_choice": tool_choice,
            }
        else:
            tools_params = {}

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            if max_output_tokens is not None:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts

        self.url = self.endpoint.api_base
        self.headers = {"Authorization": f"Bearer {self.endpoint.api_key}", "Content-Type": "application/json"}

        request_body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "stream": self.stream,
            "mask_sensitive_info": False,
            **tools_params,
            **kwargs,
        }

        if self.stream:

            def generator():
                with self.http_client.stream(
                    "POST",
                    url=self.url,
                    headers=self.headers,
                    json=request_body,
                    timeout=60,
                ) as response:
                    for chunk in response.iter_lines():
                        if chunk:
                            chunk_data = json.loads(chunk[6:])
                            if chunk_data["object"] != "chat.completion.chunk":
                                continue
                            tool_calls_params = extract_tool_calls(chunk_data)
                            has_tool_calls = True if tool_calls_params else False
                            if has_tool_calls:
                                yield ChatCompletionDeltaMessage(
                                    **{
                                        "content": chunk_data["choices"][0]["delta"].get("content"),
                                        "role": "assistant",
                                        **tool_calls_params,
                                    }
                                )
                            else:
                                yield ChatCompletionDeltaMessage(
                                    **{
                                        "content": chunk_data["choices"][0]["delta"]["content"],
                                        "role": "assistant",
                                    }
                                )

            return generator()
        else:
            response = httpx.post(
                url=self.url,
                headers=self.headers,
                json=request_body,
                timeout=60,
            )
            result = response.json()
            tool_calls_params = extract_tool_calls(result)
            return ChatCompletionMessage(
                **{
                    "content": result["choices"][0]["message"].get("content"),
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": result["usage"]["total_tokens"],
                        "total_tokens": result["usage"]["total_tokens"],
                    },
                    "role": "assistant",
                    **tool_calls_params,
                }
            )


class AsyncMiniMaxChatClient(BaseAsyncChatClient):
    DEFAULT_MODEL: str = defs.MINIMAX_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.MiniMax

    def __init__(
        self,
        model: str = defs.MINIMAX_DEFAULT_MODEL,
        stream: bool = True,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        **kwargs,
    ):
        super().__init__(
            model,
            stream,
            temperature,
            context_length_control,
            random_endpoint,
            endpoint_id,
            **kwargs,
        )
        self.http_client = httpx.AsyncClient()

    async def create_completion(
        self,
        messages: list = list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: list | None = None,
        tool_choice: str = "auto",
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature
        if isinstance(tool_choice, NotGiven):
            tool_choice = "auto"

        self.model_setting = self.backend_settings.models[self.model]
        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            tools_params = {
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": tool["function"]["name"],
                            "description": tool["function"].get("description", ""),
                            "parameters": json.dumps(tool["function"].get("parameters", {})),
                        },
                    }
                    for tool in tools
                ],
                "tool_choice": tool_choice,
            }
        else:
            tools_params = {}

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            if max_output_tokens is not None:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts

        self.url = self.endpoint.api_base
        self.headers = {"Authorization": f"Bearer {self.endpoint.api_key}", "Content-Type": "application/json"}

        request_body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "stream": self.stream,
            "mask_sensitive_info": False,
            **tools_params,
            **kwargs,
        }

        if self.stream:

            async def generator():
                async with self.http_client.stream(
                    "POST",
                    url=self.url,
                    headers=self.headers,
                    json=request_body,
                    timeout=60,
                ) as response:
                    has_tool_calls = False
                    async for chunk in response.aiter_lines():
                        if chunk:
                            chunk_data = json.loads(chunk[6:])
                            if chunk_data["object"] != "chat.completion.chunk":
                                continue
                            tool_calls_params = extract_tool_calls(chunk_data)
                            has_tool_calls = True if tool_calls_params else False
                            if has_tool_calls:
                                yield ChatCompletionDeltaMessage(
                                    **{
                                        "content": chunk_data["choices"][0]["delta"].get("content"),
                                        "role": "assistant",
                                        **tool_calls_params,
                                    }
                                )
                            else:
                                yield ChatCompletionDeltaMessage(
                                    **{
                                        "content": chunk_data["choices"][0]["delta"]["content"],
                                        "role": "assistant",
                                    }
                                )

            return generator()
        else:
            response = await self.http_client.post(
                url=self.url,
                headers=self.headers,
                json=request_body,
                timeout=60,
            )
            result = response.json()
            tool_calls_params = extract_tool_calls(result)
            return ChatCompletionMessage(
                **{
                    "content": result["choices"][0]["message"].get("content"),
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": result["usage"]["total_tokens"],
                        "total_tokens": result["usage"]["total_tokens"],
                    },
                    "role": "assistant",
                    **tool_calls_params,
                }
            )

    async def __aexit__(self, exc_type, exc, tb):
        await self.http_client.aclose()
