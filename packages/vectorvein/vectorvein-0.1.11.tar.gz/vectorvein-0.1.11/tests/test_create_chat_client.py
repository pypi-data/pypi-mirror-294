# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
import time
import asyncio

from vectorvein.settings import settings
from vectorvein.chat_clients import (
    BackendType,
    format_messages,
    create_chat_client,
    create_async_chat_client,
)

from sample_settings import sample_settings


settings.load(sample_settings)

tools_for_multiple_calls = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
        },
    }
]

messages_for_multiple_calls = [
    {
        "role": "system",
        "content": "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.",
    },
    {"role": "user", "content": "What is the current temperature of New York, San Francisco and Chicago?"},
]

tools_simple = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "video2mindmap_speech_recognition",
            "description": "输入B站视频网址后可获得\n- 语音识别的文字结果\n- 根据语音识别结果得到的内容总结",
            "parameters": {
                "type": "object",
                "required": ["url_or_bvid"],
                "properties": {"url_or_bvid": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dall_e_image_generation",
            "description": "输入一段文字，Dall-E 根据文字内容生成一张图片。",
            "parameters": {"type": "object", "required": ["prompt"], "properties": {"prompt": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gpt_vision_url_image_analysis",
            "description": "输入图像链接以及一段文字，让 GPT-Vision 根据文字和图像生成回答文字。",
            "parameters": {
                "type": "object",
                "required": ["urls", "text_prompt"],
                "properties": {
                    "urls": {"type": "string"},
                    "text_prompt": {"type": "string", "description": "文字提示"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bing_search",
            "description": "输入搜索关键词，返回Bing搜索结果",
            "parameters": {
                "type": "object",
                "required": ["search_text"],
                "properties": {
                    "search_text": {"type": "string"},
                },
            },
        },
    },
]


system = "You are a helpful assistant with access to tools."
messages_for_tools_simple = [{"role": "system", "content": system}]
messages_for_tools_simple.extend(
    [
        {
            "role": "user",
            # "content": "总结一下这个视频内容 https://www.bilibili.com/video/BV17C41187P2",
            "content": "画一个长毛橘猫图片",
            # "content": "Draw a picture of a long-haired orange cat",
            # "content": "周大福最新股价多少？",
        },
    ]
)

messages_simple = [
    {
        "role": "system",
        "content": "As an expert in SQLite, you are expected to utilize your knowledge to craft SQL queries that are in strict adherence with SQLite syntax standards when responding to inquiries.",
    },
    {
        "role": "user",
        "content": "The table structure is as follows:\n```sql\nCREATE TABLE 历年能源消费构成 (\n    年份        INTEGER,\n    煤炭        INTEGER,\n    石油        INTEGER,\n    天然气       INTEGER,\n    一次电力及其他能源 INTEGER\n);\n\n```\n\nPlease write the SQL to answer the question: `筛出2005年到2010年之间煤炭和石油的数据然后分别计算这几年煤炭消费总量和石油消费总量，放在一张表里呈现`\nDo not explain.",
    },
]


def test_sync(backend, model, stream: bool = False, use_tool: bool = False):
    client = create_chat_client(backend, model=model, stream=stream)
    if use_tool:
        messages = messages_for_tools_simple
        tools_params = {"tools": tools_simple}
    else:
        messages = messages_simple
        tools_params = {}

    if not stream:
        response = client.create_completion(messages=format_messages(messages, backend=backend), **tools_params)
        print(response)
    else:
        response = client.create_stream(messages=format_messages(messages, backend=backend), **tools_params)
        for chunk in response:
            print(chunk)
            print("=" * 20)


async def test_async(backend, model, stream: bool = False, use_tool: bool = False):
    client = create_async_chat_client(backend, model=model)
    if use_tool:
        messages = messages_for_tools_simple
        tools_params = {"tools": tools_simple}
    else:
        messages = messages_simple
        tools_params = {}

    if not stream:
        response = await client.create_completion(
            messages=format_messages(messages, backend=backend), stream=False, **tools_params
        )
        print(response)
    else:
        response = await client.create_stream(messages=format_messages(messages, backend=backend), **tools_params)
        async for chunk in response:
            print(chunk)
            print("=" * 20)


backend = BackendType.Anthropic
model = "claude-3-5-sonnet-20240620"
model = "claude-3-haiku-20240307"
model = "claude-3-opus-20240229"
model = "claude-3-opus-20240229"
model = "claude-3-5-sonnet-20240620"
backend = BackendType.DeepSeek
model = "deepseek-chat"
# backend = BackendType.Gemini
# model = "gemini-1.5-flash"
# backend = BackendType.Moonshot
# model = "moonshot-v1-8k"
# backend = BackendType.OpenAI
# model = "gpt-4o"
# model = "gpt-35-turbo"
backend = BackendType.MiniMax
model = "abab6.5s-chat"
# backend = BackendType.Yi
# model = "yi-large-fc"
# model = "yi-large-turbo"
# model = "yi-large"
# model = "yi-medium"
# model = "yi-spark"
# backend = BackendType.Qwen
# model = "qwen2-72b-instruct"
# model = "qwen1.5-72b-chat"
# backend = BackendType.ZhiPuAI
# model = "glm-4-long"
# backend = BackendType.Groq
# model = "mixtral-8x7b-32768"
# model = "llama3-70b-8192"
# model = "llama3-8b-8192"
# model = "gemma-7b-it"
# backend = BackendType.Mistral
# model = "open-mistral-7b"
# model = "open-mixtral-8x7b"
# model = "open-mixtral-8x22b"
# model = "open-mistral-nemo"
# model = "codestral-latest"
# model = "mistral-small"
# model = "mistral-medium"
# model = "mistral-large"

start_time = time.perf_counter()
# test_sync(backend=backend, model=model, stream=False, use_tool=False)
# test_sync(backend=backend, model=model, stream=False, use_tool=True)
# test_sync(backend=backend, model=model, stream=True, use_tool=False)
test_sync(backend=backend, model=model, stream=True, use_tool=True)
# asyncio.run(test_async(backend=backend, model=model, stream=False, use_tool=False))
# asyncio.run(test_async(backend=backend, model=model, stream=False, use_tool=True))
# asyncio.run(test_async(backend=backend, model=model, stream=True, use_tool=False))
# asyncio.run(test_async(backend=backend, model=model, stream=True, use_tool=True))
end_time = time.perf_counter()
print(f"Stream time elapsed: {end_time - start_time} seconds")
