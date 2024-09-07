# @Author: Bi Ying
# @Date:   2024-06-17 23:47:49
import json
import random

import httpx

from ..settings import settings
from .utils import cutoff_messages
from ..types import defaults as defs
from .base_client import BaseChatClient, BaseAsyncChatClient
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import ChatCompletionMessage, ChatCompletionDeltaMessage


class GeminiChatClient(BaseChatClient):
    DEFAULT_MODEL: str = defs.GEMINI_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.Gemini

    def __init__(
        self,
        model: str = defs.GEMINI_DEFAULT_MODEL,
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
        tools: list | None = None,
        tool_choice: str | None = None,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature

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

        if tools:
            tools_params = {"tools": [{"function_declarations": [tool["function"] for tool in tools]}]}
        else:
            tools_params = {}

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        request_body = {
            "contents": messages,
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": max_tokens,
            },
            **tools_params,
        }
        if system_prompt:
            request_body["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        headers = {"Content-Type": "application/json"}

        params = {"key": self.endpoint.api_key}

        if self.stream:
            url = f"{self.endpoint.api_base}/models/{self.model_setting.id}:streamGenerateContent"
            params["alt"] = "sse"

            def generator():
                result = {"content": ""}
                with httpx.stream("POST", url, headers=headers, params=params, json=request_body) as response:
                    for chunk in response.iter_lines():
                        message = {"content": ""}
                        if not chunk.startswith("data:"):
                            continue
                        data = json.loads(chunk[5:])
                        chunk_content = data["candidates"][0]["content"]["parts"][0]
                        if "text" in chunk_content:
                            message["content"] = chunk_content["text"]
                            result["content"] += message["content"]
                        elif "functionCall" in chunk_content:
                            message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": "call_0",
                                    "function": {
                                        "arguments": json.dumps(
                                            chunk_content["functionCall"]["args"], ensure_ascii=False
                                        ),
                                        "name": chunk_content["functionCall"]["name"],
                                    },
                                    "type": "function",
                                }
                            ]

                        result["usage"] = message["usage"] = {
                            "prompt_tokens": data["usageMetadata"]["promptTokenCount"],
                            "completion_tokens": data["usageMetadata"]["candidatesTokenCount"],
                            "total_tokens": data["usageMetadata"]["totalTokenCount"],
                        }
                        yield ChatCompletionDeltaMessage(**message)

            return generator()
        else:
            url = f"{self.endpoint.api_base}/models/{self.model_setting.id}:generateContent"
            response = httpx.post(url, json=request_body, headers=headers, params=params, timeout=None).json()
            result = {
                "content": "",
                "usage": {
                    "prompt_tokens": response.get("usageMetadata", {}).get("promptTokenCount", 0),
                    "completion_tokens": response.get("usageMetadata", {}).get("candidatesTokenCount", 0),
                    "total_tokens": response.get("usageMetadata", {}).get("totalTokenCount", 0),
                },
            }
            tool_calls = []
            for part in response["candidates"][0]["content"]["parts"]:
                if "text" in part:
                    result["content"] += part["text"]
                elif "functionCall" in part:
                    tool_call = {
                        "index": 0,
                        "id": "call_0",
                        "function": {
                            "arguments": json.dumps(part["functionCall"]["args"], ensure_ascii=False),
                            "name": part["functionCall"]["name"],
                        },
                        "type": "function",
                    }
                    tool_calls.append(tool_call)

            if tool_calls:
                result["tool_calls"] = tool_calls

            return ChatCompletionMessage(**result)


class AsyncGeminiChatClient(BaseAsyncChatClient):
    DEFAULT_MODEL: str = defs.GEMINI_DEFAULT_MODEL
    BACKEND_NAME: BackendType = BackendType.Gemini

    def __init__(
        self,
        model: str = defs.GEMINI_DEFAULT_MODEL,
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
        tools: list | None = None,
        tool_choice: str | None = None,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature

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

        if tools:
            tools_params = {"tools": [{"function_declarations": [tool["function"] for tool in tools]}]}
        else:
            tools_params = {}

        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        request_body = {
            "contents": messages,
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": max_tokens,
            },
            **tools_params,
        }
        if system_prompt:
            request_body["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        headers = {"Content-Type": "application/json"}

        params = {"key": self.endpoint.api_key}

        if self.stream:
            url = f"{self.endpoint.api_base}/models/{self.model_setting.id}:streamGenerateContent"
            params["alt"] = "sse"

            async def generator():
                result = {"content": ""}
                client = httpx.AsyncClient()
                async with client.stream("POST", url, headers=headers, params=params, json=request_body) as response:
                    async for chunk in response.aiter_lines():
                        message = {"content": ""}
                        if not chunk.startswith("data:"):
                            continue
                        data = json.loads(chunk[5:])
                        chunk_content = data["candidates"][0]["content"]["parts"][0]
                        if "text" in chunk_content:
                            message["content"] = chunk_content["text"]
                            result["content"] += message["content"]
                        elif "functionCall" in chunk_content:
                            message["tool_calls"] = [
                                {
                                    "index": 0,
                                    "id": "call_0",
                                    "function": {
                                        "arguments": json.dumps(
                                            chunk_content["functionCall"]["args"], ensure_ascii=False
                                        ),
                                        "name": chunk_content["functionCall"]["name"],
                                    },
                                    "type": "function",
                                }
                            ]

                        result["usage"] = message["usage"] = {
                            "prompt_tokens": data["usageMetadata"]["promptTokenCount"],
                            "completion_tokens": data["usageMetadata"]["candidatesTokenCount"],
                            "total_tokens": data["usageMetadata"]["totalTokenCount"],
                        }
                        yield ChatCompletionDeltaMessage(**message)

            return generator()
        else:
            url = f"{self.endpoint.api_base}/models/{self.model_setting.id}:generateContent"
            async with httpx.AsyncClient(headers=headers, params=params, timeout=None) as client:
                response = await client.post(url, json=request_body)
                response = response.json()
                result = {
                    "content": "",
                    "usage": {
                        "prompt_tokens": response.get("usageMetadata", {}).get("promptTokenCount", 0),
                        "completion_tokens": response.get("usageMetadata", {}).get("candidatesTokenCount", 0),
                        "total_tokens": response.get("usageMetadata", {}).get("totalTokenCount", 0),
                    },
                }
                tool_calls = []
                for part in response["candidates"][0]["content"]["parts"]:
                    if "text" in part:
                        result["content"] += part["text"]
                    elif "functionCall" in part:
                        tool_call = {
                            "index": 0,
                            "id": "call_0",
                            "function": {
                                "arguments": json.dumps(part["functionCall"]["args"], ensure_ascii=False),
                                "name": part["functionCall"]["name"],
                            },
                            "type": "function",
                        }
                        tool_calls.append(tool_call)

                if tool_calls:
                    result["tool_calls"] = tool_calls

                return ChatCompletionMessage(**result)
