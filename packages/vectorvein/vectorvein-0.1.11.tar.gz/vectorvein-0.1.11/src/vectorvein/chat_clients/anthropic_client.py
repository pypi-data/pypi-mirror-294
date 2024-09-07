# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
import json
import random

from openai._types import NotGiven as OpenAINotGiven
from anthropic import Anthropic, AnthropicVertex, AsyncAnthropic, AsyncAnthropicVertex
from anthropic._types import NotGiven, NOT_GIVEN
from anthropic.types import (
    TextBlock,
    ToolUseBlock,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    RawContentBlockStartEvent,
    RawContentBlockDeltaEvent,
)
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth import _helpers

from ..settings import settings
from ..types import defaults as defs
from .utils import cutoff_messages, get_token_counts
from .base_client import BaseChatClient, BaseAsyncChatClient
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import ChatCompletionMessage, ChatCompletionDeltaMessage


def refactor_tool_use_params(tools: list):
    return [
        {
            "name": tool["function"]["name"],
            "description": tool["function"]["description"],
            "input_schema": tool["function"]["parameters"],
        }
        for tool in tools
    ]


def refactor_tool_calls(tool_calls: list):
    return [
        {
            "index": index,
            "id": tool["id"],
            "type": "function",
            "function": {
                "name": tool["name"],
                "arguments": json.dumps(tool["input"], ensure_ascii=False),
            },
        }
        for index, tool in enumerate(tool_calls)
    ]


def format_messages_alternate(messages: list) -> list:
    # messages: roles must alternate between "user" and "assistant", and not multiple "user" roles in a row
    # reformat multiple "user" roles in a row into {"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}, {"type": "text", "text": "How are you?"}]}
    # same for assistant role
    # if not multiple "user" or "assistant" roles in a row, keep it as is

    formatted_messages = []
    current_role = None
    current_content = []

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role != current_role:
            if current_content:
                formatted_messages.append({"role": current_role, "content": current_content})
                current_content = []
            current_role = role

        if isinstance(content, str):
            current_content.append({"type": "text", "text": content})
        elif isinstance(content, list):
            current_content.extend(content)
        else:
            current_content.append(content)

    if current_content:
        formatted_messages.append({"role": current_role, "content": current_content})

    return formatted_messages


class AnthropicChatClient(BaseChatClient):
    DEFAULT_MODEL: str = defs.ANTHROPIC_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.Anthropic

    def __init__(
        self,
        model: str = defs.ANTHROPIC_DEFAULT_MODEL,
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

    def create_completion(
        self,
        messages: list = list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature
        if isinstance(tools, OpenAINotGiven):
            tools = NOT_GIVEN
        if isinstance(tool_choice, OpenAINotGiven):
            tool_choice = NOT_GIVEN

        self.model_setting = self.backend_settings.models[self.model]

        if messages[0].get("role") == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
        else:
            system_prompt = ""

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        messages = format_messages_alternate(messages)

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_vertex:
            self.creds = Credentials(
                token=self.endpoint.credentials.get("token"),
                refresh_token=self.endpoint.credentials.get("refresh_token"),
                token_uri=self.endpoint.credentials.get("token_uri"),
                scopes=None,
                client_id=self.endpoint.credentials.get("client_id"),
                client_secret=self.endpoint.credentials.get("client_secret"),
                quota_project_id=self.endpoint.credentials.get("quota_project_id"),
                expiry=_helpers.utcnow() - _helpers.REFRESH_THRESHOLD,
                rapt_token=self.endpoint.credentials.get("rapt_token"),
                trust_boundary=self.endpoint.credentials.get("trust_boundary"),
                universe_domain=self.endpoint.credentials.get("universe_domain"),
                account=self.endpoint.credentials.get("account", ""),
            )

            if self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            if self.endpoint.api_base is None:
                base_url = None
            else:
                base_url = f"{self.endpoint.api_base}{self.endpoint.region}-aiplatform/v1"

            self._client = AnthropicVertex(
                region=self.endpoint.region,
                base_url=base_url,
                project_id=self.endpoint.credentials.get("quota_project_id"),
                access_token=self.creds.token,
            )
        else:
            self._client = Anthropic(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
            )

        tools_params = refactor_tool_use_params(tools) if tools else tools

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            if max_output_tokens is not None:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts

        response = self._client.messages.create(
            model=self.model_setting.id,
            messages=messages,
            system=system_prompt,
            stream=self.stream,
            temperature=self.temperature,
            max_tokens=max_tokens,
            tools=tools_params,
            tool_choice=tool_choice,
            **kwargs,
        )

        if self.stream:

            def generator():
                result = {"content": ""}
                for chunk in response:
                    message = {"content": ""}
                    if isinstance(chunk, RawMessageStartEvent):
                        result["usage"] = {"prompt_tokens": chunk.message.usage.input_tokens}
                        continue
                    elif isinstance(chunk, RawContentBlockStartEvent):
                        if chunk.content_block.type == "tool_use":
                            result["tool_calls"] = message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": chunk.content_block.id,
                                    "function": {
                                        "arguments": "",
                                        "name": chunk.content_block.name,
                                    },
                                    "type": "function",
                                }
                            ]
                        elif chunk.content_block.type == "text":
                            message["content"] = chunk.content_block.text
                        yield ChatCompletionDeltaMessage(**message)
                    elif isinstance(chunk, RawContentBlockDeltaEvent):
                        if chunk.delta.type == "text_delta":
                            message["content"] = chunk.delta.text
                            result["content"] += chunk.delta.text
                        elif chunk.delta.type == "input_json_delta":
                            result["tool_calls"][0]["function"]["arguments"] += chunk.delta.partial_json
                            message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": result["tool_calls"][0]["id"],
                                    "function": {
                                        "arguments": chunk.delta.partial_json,
                                        "name": result["tool_calls"][0]["function"]["name"],
                                    },
                                    "type": "function",
                                }
                            ]
                        yield ChatCompletionDeltaMessage(**message)
                    elif isinstance(chunk, RawMessageDeltaEvent):
                        result["usage"]["completion_tokens"] = chunk.usage.output_tokens
                        result["usage"]["total_tokens"] = (
                            result["usage"]["prompt_tokens"] + result["usage"]["completion_tokens"]
                        )
                        yield ChatCompletionDeltaMessage(usage=result["usage"])

            return generator()
        else:
            result = {
                "content": "",
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
                },
            }
            tool_calls = []
            for content_block in response.content:
                if isinstance(content_block, TextBlock):
                    result["content"] += content_block.text
                elif isinstance(content_block, ToolUseBlock):
                    tool_calls.append(content_block.model_dump())

            if tool_calls:
                result["tool_calls"] = refactor_tool_calls(tool_calls)

            return ChatCompletionMessage(**result)


class AsyncAnthropicChatClient(BaseAsyncChatClient):
    DEFAULT_MODEL: str = defs.ANTHROPIC_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.Anthropic

    def __init__(
        self,
        model: str = defs.ANTHROPIC_DEFAULT_MODEL,
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

    async def create_completion(
        self,
        messages: list = list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: list | NotGiven = NOT_GIVEN,
        tool_choice: str | NotGiven = NOT_GIVEN,
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature
        if isinstance(tools, OpenAINotGiven):
            tools = NOT_GIVEN
        if isinstance(tool_choice, OpenAINotGiven):
            tool_choice = NOT_GIVEN

        self.model_setting = self.backend_settings.models[self.model]

        if messages[0].get("role") == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
        else:
            system_prompt = ""

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        messages = format_messages_alternate(messages)

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_vertex:
            self.creds = Credentials(
                token=self.endpoint.credentials.get("token"),
                refresh_token=self.endpoint.credentials.get("refresh_token"),
                token_uri=self.endpoint.credentials.get("token_uri"),
                scopes=None,
                client_id=self.endpoint.credentials.get("client_id"),
                client_secret=self.endpoint.credentials.get("client_secret"),
                quota_project_id=self.endpoint.credentials.get("quota_project_id"),
                expiry=_helpers.utcnow() - _helpers.REFRESH_THRESHOLD,
                rapt_token=self.endpoint.credentials.get("rapt_token"),
                trust_boundary=self.endpoint.credentials.get("trust_boundary"),
                universe_domain=self.endpoint.credentials.get("universe_domain"),
                account=self.endpoint.credentials.get("account", ""),
            )

            if self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            if self.endpoint.api_base is None:
                base_url = None
            else:
                base_url = f"{self.endpoint.api_base}{self.endpoint.region}-aiplatform/v1"

            self._client = AsyncAnthropicVertex(
                region=self.endpoint.region,
                base_url=base_url,
                project_id=self.endpoint.credentials.get("quota_project_id"),
                access_token=self.creds.token,
            )
        else:
            self._client = AsyncAnthropic(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
            )

        tools_params = refactor_tool_use_params(tools) if tools else tools

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            if max_output_tokens is not None:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                token_counts = get_token_counts({"messages": messages, "tools_params": tools_params})
                max_tokens = self.model_setting.context_length - token_counts

        response = await self._client.messages.create(
            model=self.model_setting.id,
            messages=messages,
            system=system_prompt,
            stream=self.stream,
            temperature=self.temperature,
            max_tokens=max_tokens,
            tools=tools_params,
            tool_choice=tool_choice,
            **kwargs,
        )

        if self.stream:

            async def generator():
                result = {"content": ""}
                async for chunk in response:
                    message = {"content": ""}
                    if isinstance(chunk, RawMessageStartEvent):
                        result["usage"] = {"prompt_tokens": chunk.message.usage.input_tokens}
                        continue
                    elif isinstance(chunk, RawContentBlockStartEvent):
                        if chunk.content_block.type == "tool_use":
                            result["tool_calls"] = message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": chunk.content_block.id,
                                    "function": {
                                        "arguments": "",
                                        "name": chunk.content_block.name,
                                    },
                                    "type": "function",
                                }
                            ]
                        elif chunk.content_block.type == "text":
                            message["content"] = chunk.content_block.text
                        yield ChatCompletionDeltaMessage(**message)
                    elif isinstance(chunk, RawContentBlockDeltaEvent):
                        if chunk.delta.type == "text_delta":
                            message["content"] = chunk.delta.text
                            result["content"] += chunk.delta.text
                        elif chunk.delta.type == "input_json_delta":
                            result["tool_calls"][0]["function"]["arguments"] += chunk.delta.partial_json
                            message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": result["tool_calls"][0]["id"],
                                    "function": {
                                        "arguments": chunk.delta.partial_json,
                                        "name": result["tool_calls"][0]["function"]["name"],
                                    },
                                    "type": "function",
                                }
                            ]
                        yield ChatCompletionDeltaMessage(**message)
                    elif isinstance(chunk, RawMessageDeltaEvent):
                        result["usage"]["completion_tokens"] = chunk.usage.output_tokens
                        result["usage"]["total_tokens"] = (
                            result["usage"]["prompt_tokens"] + result["usage"]["completion_tokens"]
                        )
                        yield ChatCompletionDeltaMessage(usage=result["usage"])

            return generator()
        else:
            result = {
                "content": "",
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
                },
            }
            tool_calls = []
            for content_block in response.content:
                if isinstance(content_block, TextBlock):
                    result["content"] += content_block.text
                elif isinstance(content_block, ToolUseBlock):
                    tool_calls.append(content_block.model_dump())

            if tool_calls:
                result["tool_calls"] = refactor_tool_calls(tool_calls)

            return ChatCompletionMessage(**result)
