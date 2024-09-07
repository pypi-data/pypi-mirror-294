# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
import json
import random

from openai._types import NotGiven, NOT_GIVEN
from openai._streaming import Stream, AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai import OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI

from .base_client import BaseChatClient, BaseAsyncChatClient
from .utils import (
    cutoff_messages,
    get_token_counts,
    ToolCallContentProcessor,
    generate_tool_use_system_prompt,
)
from ..settings import settings
from ..types import defaults as defs
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import ChatCompletionMessage, ChatCompletionDeltaMessage


class OpenAICompatibleChatClient(BaseChatClient):
    DEFAULT_MODEL: str = ""
    BACKEND_NAME: BackendType

    def __init__(
        self,
        model: str = "",
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

        self.model_setting = self.backend_settings.models[self.model]

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_azure:
            self._client = AzureOpenAI(
                azure_endpoint=self.endpoint.api_base,
                api_key=self.endpoint.api_key,
                api_version="2024-05-01-preview",
            )
        else:
            self._client = OpenAI(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
            )

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            if self.model_setting.function_call_available:
                tools_params = dict(tools=tools, tool_choice=tool_choice)
            else:
                tools_str = json.dumps(tools, ensure_ascii=False, indent=None)
                additional_system_prompt = generate_tool_use_system_prompt(tools=tools_str)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] += "\n\n" + additional_system_prompt
                else:
                    messages.insert(0, {"role": "system", "content": additional_system_prompt})
                tools_params = {}
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

        response: ChatCompletion | Stream[ChatCompletionChunk] = self._client.chat.completions.create(
            model=self.model_setting.id,
            messages=messages,
            stream=self.stream,
            temperature=self.temperature,
            max_tokens=max_tokens,
            **tools_params,
            **kwargs,
        )

        if self.stream:

            def generator():
                full_content = ""
                result = {}
                for chunk in response:
                    if len(chunk.choices) == 0:
                        continue
                    if not chunk.choices[0].delta:
                        continue
                    if self.model_setting.function_call_available:
                        if chunk.choices[0].delta.tool_calls:
                            for index, tool_call in enumerate(chunk.choices[0].delta.tool_calls):
                                tool_call.index = index
                        yield ChatCompletionDeltaMessage(**chunk.choices[0].delta.model_dump())
                    else:
                        message = chunk.choices[0].delta.model_dump()
                        full_content += message["content"] if message["content"] else ""
                        if tools:
                            tool_call_data = ToolCallContentProcessor(full_content).tool_calls
                            if tool_call_data:
                                message["tool_calls"] = tool_call_data["tool_calls"]
                        if full_content in ("<", "<|", "<|▶", "<|▶|") or full_content.startswith("<|▶|>"):
                            message["content"] = ""
                            result = message
                            continue
                        yield ChatCompletionDeltaMessage(**message)
                if result:
                    yield ChatCompletionDeltaMessage(**result)

            return generator()
        else:
            result = {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump(),
            }
            if tools:
                if self.model_setting.function_call_available and response.choices[0].message.tool_calls:
                    result["tool_calls"] = [
                        {**tool_call.model_dump(), "type": "function"}
                        for tool_call in response.choices[0].message.tool_calls
                    ]
                else:
                    tool_call_content_processor = ToolCallContentProcessor(result["content"])
                    tool_call_data = tool_call_content_processor.tool_calls
                    if tool_call_data:
                        result["tool_calls"] = tool_call_data["tool_calls"]
                        result["content"] = tool_call_content_processor.non_tool_content

            return ChatCompletionMessage(**result)


class AsyncOpenAICompatibleChatClient(BaseAsyncChatClient):
    DEFAULT_MODEL: str = ""
    BACKEND_NAME: BackendType

    def __init__(
        self,
        model: str = "",
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

        self.model_setting = self.backend_settings.models[self.model]

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_azure:
            self._client = AsyncAzureOpenAI(
                azure_endpoint=self.endpoint.api_base,
                api_key=self.endpoint.api_key,
                api_version="2024-05-01-preview",
            )
        else:
            self._client = AsyncOpenAI(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
            )

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            if self.model_setting.function_call_available:
                tools_params = dict(tools=tools, tool_choice=tool_choice)
            else:
                tools_str = json.dumps(tools, ensure_ascii=False, indent=None)
                additional_system_prompt = generate_tool_use_system_prompt(tools=tools_str)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] += "\n\n" + additional_system_prompt
                else:
                    messages.insert(0, {"role": "system", "content": additional_system_prompt})
                tools_params = {}
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

        response: ChatCompletion | AsyncStream[ChatCompletionChunk] = await self._client.chat.completions.create(
            model=self.model_setting.id,
            messages=messages,
            stream=self.stream,
            temperature=self.temperature,
            max_tokens=max_tokens,
            **tools_params,
            **kwargs,
        )

        if self.stream:

            async def generator():
                full_content = ""
                result = {}
                async for chunk in response:
                    if len(chunk.choices) == 0:
                        continue
                    if not chunk.choices[0].delta:
                        continue
                    if self.model_setting.function_call_available:
                        if chunk.choices[0].delta.tool_calls:
                            for index, tool_call in enumerate(chunk.choices[0].delta.tool_calls):
                                tool_call.index = index
                        yield ChatCompletionDeltaMessage(**chunk.choices[0].delta.model_dump())
                    else:
                        message = chunk.choices[0].delta.model_dump()
                        full_content += message["content"] if message["content"] else ""
                        if tools:
                            tool_call_data = ToolCallContentProcessor(full_content).tool_calls
                            if tool_call_data:
                                message["tool_calls"] = tool_call_data["tool_calls"]
                        if full_content in ("<", "<|", "<|▶", "<|▶|") or full_content.startswith("<|▶|>"):
                            message["content"] = ""
                            result = message
                            continue
                        yield ChatCompletionDeltaMessage(**message)
                if result:
                    yield ChatCompletionDeltaMessage(**result)

            return generator()
        else:
            result = {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump(),
            }
            if tools:
                if self.model_setting.function_call_available and response.choices[0].message.tool_calls:
                    result["tool_calls"] = [
                        {**tool_call.model_dump(), "type": "function"}
                        for tool_call in response.choices[0].message.tool_calls
                    ]
                else:
                    tool_call_content_processor = ToolCallContentProcessor(result["content"])
                    tool_call_data = tool_call_content_processor.tool_calls
                    if tool_call_data:
                        result["tool_calls"] = tool_call_data["tool_calls"]
                        result["content"] = tool_call_content_processor.non_tool_content
            return ChatCompletionMessage(**result)
