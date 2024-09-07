# @Author: Bi Ying
# @Date:   2024-07-27 18:26:05
sample_settings = {
    "endpoints": [
        {
            "id": "moonshot-default",
            "api_base": "https://api.moonshot.cn/v1",
            "api_key": "",
            "rpm": 30,
            "tpm": 3000000,
            "concurrent_requests": 30,
        },
        {
            "id": "azure-openai",
            "region": "East US",
            "api_base": "",
            "endpoint_name": "",
            "api_key": "",
            "rpm": 900,
            "tpm": 150000,
            "is_azure": True,
        },
        {
            "id": "vertex-anthropic",
            "region": "europe-west1",
            "api_base": "",
            "credentials": {},
            "is_vertex": True,
        },
        {
            "id": "minimax-default",
            "api_base": "https://api.minimax.chat/v1/text/chatcompletion_v2",
            "api_key": "",
        },
        {
            "id": "gemini-default",
            "api_base": "",
            "api_key": "",
        },
        {
            "id": "deepseek-default",
            "api_base": "https://api.deepseek.com/v1",
            "api_key": "",
        },
        {
            "id": "groq-default",
            "api_base": "",
            "api_key": "",
        },
        {
            "id": "mistral-default",
            "api_base": "https://api.mistral.ai/v1",
            "api_key": "",
        },
        {
            "id": "lingyiwanwu-default",
            "api_base": "https://api.lingyiwanwu.com/v1",
            "api_key": "",
        },
        {
            "id": "zhipuai-default",
            "api_base": "https://open.bigmodel.cn/api/paas/v4",
            "api_key": "",
        },
    ],
    "moonshot": {
        "models": {
            "moonshot-custom": {
                "id": "moonshot-v1-8k",
                "endpoints": ["moonshot-default"],
                "function_call_available": True,
                "response_format_available": True,
                "context_length": 8000,
                "max_output_tokens": 4000,
            },
            "moonshot-v1-8k": {"endpoints": ["moonshot-default"]},
            "moonshot-v1-32k": {"endpoints": ["moonshot-default"]},
            "moonshot-v1-128k": {"endpoints": ["moonshot-default"]},
        }
    },
    "openai": {
        "models": {
            "gpt-4o": {
                "id": "gpt-4o",
                "endpoints": ["azure-openai"],
            },
            "gpt-4": {
                "id": "gpt-4",
                "endpoints": ["azure-openai"],
            },
            "gpt-35-turbo": {
                "id": "gpt-35-turbo",
                "endpoints": ["azure-openai"],
            },
        }
    },
    "anthropic": {
        "models": {
            "claude-3-opus-20240229": {
                "id": "claude-3-opus-20240229",
                "endpoints": ["vertex-anthropic"],
            },
            "claude-3-sonnet-20240229": {
                "id": "claude-3-sonnet-20240229",
                "endpoints": ["vertex-anthropic"],
            },
            "claude-3-haiku-20240307": {
                "id": "claude-3-haiku-20240307",
                "endpoints": ["vertex-anthropic"],
            },
            "claude-3-5-sonnet-20240620": {
                "id": "claude-3-5-sonnet@20240620",
                "endpoints": ["vertex-anthropic"],
            },
        }
    },
    "minimax": {"models": {"abab6.5s-chat": {"id": "abab6.5s-chat", "endpoints": ["minimax-default"]}}},
    "gemini": {
        "models": {
            "gemini-1.5-pro": {"id": "gemini-1.5-pro", "endpoints": ["gemini-default"]},
            "gemini-1.5-flash": {"id": "gemini-1.5-flash", "endpoints": ["gemini-default"]},
        }
    },
    "deepseek": {
        "models": {
            "deepseek-chat": {"id": "deepseek-chat", "endpoints": ["deepseek-default"]},
            "deepseek-coder": {"id": "deepseek-coder", "endpoints": ["deepseek-default"]},
        },
    },
    "groq": {
        "models": {
            "mixtral-8x7b-32768": {"id": "mixtral-8x7b-32768", "endpoints": ["groq-default"]},
            "llama3-70b-8192": {"id": "llama3-70b-8192", "endpoints": ["groq-default"]},
            "llama3-8b-8192": {"id": "llama3-8b-8192", "endpoints": ["groq-default"]},
            "gemma-7b-it": {"id": "gemma-7b-it", "endpoints": ["groq-default"]},
        },
    },
    "mistral": {
        "models": {
            "mistral-small-latest": {
                "id": "mistral-small-latest",
                "context_length": 30000,
                "function_call_available": True,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
            "mistral-medium-latest": {
                "id": "mistral-medium-latest",
                "context_length": 30000,
                "function_call_available": False,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
            "mistral-large-latest": {
                "id": "mistral-large-latest",
                "context_length": 128000,
                "function_call_available": True,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
        },
    },
    "yi": {
        "models": {
            "yi-large": {
                "id": "yi-large",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-large-turbo": {
                "id": "yi-large-turbo",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-large-fc": {
                "id": "yi-large-fc",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-medium": {
                "id": "yi-medium",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-medium-200k": {
                "id": "yi-medium-200k",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-spark": {
                "id": "yi-spark",
                "endpoints": ["lingyiwanwu-default"],
            },
            "yi-vision": {
                "id": "yi-vision",
                "endpoints": ["lingyiwanwu-default"],
            },
        },
    },
    "zhipuai": {
        "models": {
            "glm-3-turbo": {
                "id": "glm-3-turbo",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4": {
                "id": "glm-4",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4-0520": {
                "id": "glm-4-0520",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4-air": {
                "id": "glm-4-air",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4-airx": {
                "id": "glm-4-airx",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4-flash": {
                "id": "glm-4-flash",
                "endpoints": ["zhipuai-default"],
            },
            "glm-4v": {
                "id": "glm-4v",
                "endpoints": ["zhipuai-default"],
            },
        },
    },
}

sample_settings = {
    "endpoints": [
        {
            "id": "moonshot-default",
            "api_base": "https://api.moonshot.cn/v1",
            "api_key": "Y2xwbG9jNTB0YzEwYmc0MHRrNmc6bXNrLXN6OFBZZ2NicEZCZ2hUMlRJU2NQeVNTd1FEeVI=",
            "rpm": 30,
            "tpm": 3000000,
            "concurrent_requests": 30,
        },
        {
            "id": "azure-openai-vectorvein-east-us",
            "region": "East US",
            "api_base": "https://vectorvein-east-us.openai.azure.com/",
            "endpoint_name": "vectorvein-east-us",
            "api_key": "57f4af89bb744d44be407aaea3ee2a88",
            "rpm": 900,
            "tpm": 150000,
            "is_azure": True,
        },
        {
            "id": "azure-openai-vectorvein-noth-central-us",
            "region": "North Central US",
            "api_base": "https://vectorvein-north-central-us.openai.azure.com/",
            "endpoint_name": "vectorvein-north-central-us",
            "api_key": "e260ed4195dc415bafad14e9463a82a5",
            "rpm": 900,
            "tpm": 150000,
            "is_azure": True,
        },
        {
            "id": "azure-openai-vectorvein-west-us",
            "region": "West US",
            "api_base": "https://vectorvein-west-us.openai.azure.com/",
            "endpoint_name": "vectorvein-west-us",
            "api_key": "5934e58d0637456ab644960fe5506ca8",
            "rpm": 900,
            "tpm": 150000,
            "is_azure": True,
        },
        {
            "id": "azure-openai-vectorvein-east-us-2",
            "region": "East US 2",
            "api_base": "https://vectorvein-east-us-2.openai.azure.com/",
            "endpoint_name": "vectorvein-east-us-2",
            "api_key": "363e5d12b3824090b66115a7d4214c89",
            "rpm": 900,
            "tpm": 150000,
            "is_azure": True,
        },
        {
            "id": "azure-openai-vectorvein-au-east",
            "region": "Australia East",
            "api_base": "https://vectorvein-au-east.openai.azure.com",
            "endpoint_name": "vectorvein-au-east",
            "api_key": "726c05228236484a91496be6e1c704eb",
            "rpm": 480,
            "tpm": 80000,
            "is_azure": True,
        },
        {
            "id": "vertex-anthropic-vectorvein-europe-west1",
            "region": "europe-west1",
            "api_base": "https://googleapis-subdomain.pages.dev/",
            "credentials": {
                "account": "",
                "token_uri": "https://vectorvein-oauth2-googleapis.pages.dev/token",
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
                "quota_project_id": "claude-420106",
                "refresh_token": "1//0g7B8-kg6qgXyCgYIARAAGBASNwF-L9Irnn4WxFpE9__nMKcF4AbyIOi84ZXBMcsG48w99rw1vywbEUI9L6z2YQiyt3KOySnexTo",
                "type": "authorized_user",
                "universe_domain": "googleapis.com",
            },
            "is_vertex": True,
        },
        {
            "id": "vertex-anthropic-vectorvein-us-central1",
            "region": "us-central1",
            "api_base": "https://googleapis-subdomain.pages.dev/",
            "credentials": {
                "account": "",
                "token_uri": "https://vectorvein-oauth2-googleapis.pages.dev/token",
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
                "quota_project_id": "claude-420106",
                "refresh_token": "1//0g7B8-kg6qgXyCgYIARAAGBASNwF-L9Irnn4WxFpE9__nMKcF4AbyIOi84ZXBMcsG48w99rw1vywbEUI9L6z2YQiyt3KOySnexTo",
                "type": "authorized_user",
                "universe_domain": "googleapis.com",
            },
            "is_vertex": True,
        },
        {
            "id": "vertex-anthropic-vectorvein-asia-southeast1",
            "region": "asia-southeast1",
            "api_base": "https://googleapis-subdomain.pages.dev/",
            "credentials": {
                "account": "",
                "token_uri": "https://vectorvein-oauth2-googleapis.pages.dev/token",
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
                "quota_project_id": "claude-420106",
                "refresh_token": "1//0g7B8-kg6qgXyCgYIARAAGBASNwF-L9Irnn4WxFpE9__nMKcF4AbyIOi84ZXBMcsG48w99rw1vywbEUI9L6z2YQiyt3KOySnexTo",
                "type": "authorized_user",
                "universe_domain": "googleapis.com",
            },
            "is_vertex": True,
        },
        {
            "id": "vertex-anthropic-vectorvein-us-east5",
            "region": "us-east5",
            "api_base": "https://googleapis-subdomain.pages.dev/",
            "credentials": {
                "account": "",
                "token_uri": "https://vectorvein-oauth2-googleapis.pages.dev/token",
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
                "quota_project_id": "claude-420106",
                "refresh_token": "1//0g7B8-kg6qgXyCgYIARAAGBASNwF-L9Irnn4WxFpE9__nMKcF4AbyIOi84ZXBMcsG48w99rw1vywbEUI9L6z2YQiyt3KOySnexTo",
                "type": "authorized_user",
                "universe_domain": "googleapis.com",
            },
            "is_vertex": True,
        },
        {
            "id": "minimax-default",
            "api_base": "https://api.minimax.chat/v1/text/chatcompletion_v2",
            "api_key": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoidmVjdG9ydmVpbiIsIlN1YmplY3RJRCI6IjE2ODczMzQ1NTQ4NzMxNjkiLCJQaG9uZSI6Ik1UVXlNVEExT1RBNE16ST0iLCJHcm91cElEIjoiMTY4NzMzNDU1NDQxOTE4NyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6ImJpeWluZ0B0aW5ndGFsa3MuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjMtMDYtMjEgMTY6MjI6MDkiLCJpc3MiOiJtaW5pbWF4In0.jeptv5f2GSB6UrYZF-DBS9t0F4-is2d4Z3wqe2iA-cWto3VNholf1xCWOU61uNkzbvNEX7QhhGvyed_u7W6Z94t5XdIDIZpVnhmKS2El0FGDoaC63XF5dTtXgrFg5R3hUxMqbC6af8V-FR-AdIvhtW_vQmlNNO2NCSyCTpR1hSnETAdq1JErV7mjwEhi0QJevm_LVXcWJ0-2By3eIvc4cP0oZ2XDXBTtNj1kMC72W7HfqcNbXpcWsOgVOldOhTV2Yag_77dWaPlFwvz3b8ySK6CrNyhNgk2OFmj556R4VT7AlDL5IkTPz2iRsvB6x8sAzOxspZbUfAY8c5Hn13Hh-Q",
        },
        {
            "id": "gemini-default",
            "api_base": "https://vectorvein-gemini.pages.dev/v1beta",
            "api_key": "AIzaSyAmMpIYtRsQqulOVJvfQ0ctKMSMXAdY5xw",
        },
        {
            "id": "deepseek-default",
            "api_base": "https://api.deepseek.com/v1",
            "api_key": "sk-6dad42e7154743cd80b77dff5d0ecaaa",
        },
        {
            "id": "groq-default",
            "api_base": "https://vectorvein-groq.pages.dev/openai/v1",
            "api_key": "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",
        },
        {
            "id": "mistral-default",
            "api_base": "https://api.mistral.ai/v1",
            "api_key": "7fIGcygGYHjiEyCiijWgB3CNWvepOFjb",
        },
        {
            "id": "together-default",
            "api_base": "https://api.together.xyz/v1",
            "api_key": "bb028183093cd22c9c9e7aa108b43a1eeb103e1954e3be8c06665756ca0d76cc",
        },
        {
            "id": "lingyiwanwu-default",
            "api_base": "https://api.lingyiwanwu.com/v1",
            "api_key": "15eb1320966748518702ee7167f87429",
        },
        {
            "id": "zhipuai-default",
            "api_base": "https://open.bigmodel.cn/api/paas/v4",
            "api_key": "6bc7b05100ca83d062d4af2dd0331e7a.u2U0kz1Ip2MilIDQ",
        },
        {
            "id": "siliconflow",
            "api_base": "https://api.siliconflow.cn/v1",
            "api_key": "sk-ewmzcvzrandjdqcpvtbmxnunklayxbrzcxzgbfegxbkiqucf",
        },
    ],
    "moonshot": {
        "models": {
            "moonshot-v1-8k": {"endpoints": ["moonshot-default"]},
            "moonshot-v1-32k": {"endpoints": ["moonshot-default"]},
            "moonshot-v1-128k": {"endpoints": ["moonshot-default"]},
        }
    },
    "openai": {
        "models": {
            "gpt-4o": {
                "id": "gpt-4o",
                "endpoints": [
                    "azure-openai-vectorvein-noth-central-us",
                    "azure-openai-vectorvein-west-us",
                ],
            },
            "gpt-4o-mini": {"id": "gpt-4o-mini", "endpoints": ["azure-openai-vectorvein-east-us"]},
            "gpt-4": {
                "id": "gpt-4",
                "endpoints": [
                    "azure-openai-vectorvein-east-us",
                    "azure-openai-vectorvein-east-us-2",
                    "azure-openai-vectorvein-au-east",
                ],
            },
            "gpt-35-turbo": {
                "id": "gpt-35-turbo",
                "endpoints": [
                    "azure-openai-vectorvein-east-us",
                    "azure-openai-vectorvein-au-east",
                ],
            },
        }
    },
    "anthropic": {
        "models": {
            "claude-3-opus-20240229": {
                "id": "claude-3-opus@20240229",
                "endpoints": ["vertex-anthropic-vectorvein-us-east5"],
            },
            "claude-3-sonnet-20240229": {
                "id": "claude-3-sonnet@20240229",
                "endpoints": ["vertex-anthropic-vectorvein-asia-southeast1"],
            },
            "claude-3-haiku-20240307": {
                "id": "claude-3-haiku@20240307",
                "endpoints": ["vertex-anthropic-vectorvein-us-central1"],
            },
            "claude-3-5-sonnet-20240620": {
                "id": "claude-3-5-sonnet@20240620",
                "endpoints": ["vertex-anthropic-vectorvein-europe-west1"],
            },
        }
    },
    "minimax": {
        "models": {
            "abab5-chat": {"id": "abab5-chat", "endpoints": ["minimax-default"]},
            "abab5.5-chat": {"id": "abab5.5-chat", "endpoints": ["minimax-default"]},
            "abab6-chat": {"id": "abab6-chat", "endpoints": ["minimax-default"]},
            "abab6.5s-chat": {"id": "abab6.5s-chat", "endpoints": ["minimax-default"]},
        }
    },
    "gemini": {
        "models": {
            "gemini-1.5-pro": {"id": "gemini-1.5-pro", "endpoints": ["gemini-default"]},
            "gemini-1.5-flash": {"id": "gemini-1.5-flash", "endpoints": ["gemini-default"]},
        }
    },
    "deepseek": {
        "models": {
            "deepseek-chat": {"id": "deepseek-chat", "endpoints": ["deepseek-default"]},
            "deepseek-coder": {"id": "deepseek-coder", "endpoints": ["deepseek-default"]},
        }
    },
    "groq": {
        "models": {
            "mixtral-8x7b-32768": {"id": "mixtral-8x7b-32768", "endpoints": ["groq-default"]},
            "llama3-70b-8192": {"id": "llama3-70b-8192", "endpoints": ["groq-default"]},
            "llama3-8b-8192": {"id": "llama3-8b-8192", "endpoints": ["groq-default"]},
            "gemma-7b-it": {"id": "gemma-7b-it", "endpoints": ["groq-default"]},
        }
    },
    "mistral": {
        "models": {
            "mixtral-8x7b": {
                "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "context_length": 32000,
                "function_call_available": False,
                "response_format_available": True,
                "endpoints": ["together-default"],
            },
            "mistral-small": {
                "id": "mistral-small-latest",
                "context_length": 30000,
                "function_call_available": True,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
            "mistral-medium": {
                "id": "mistral-medium-latest",
                "context_length": 30000,
                "function_call_available": False,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
            "mistral-large": {
                "id": "mistral-large-latest",
                "context_length": 128000,
                "function_call_available": True,
                "response_format_available": True,
                "endpoints": ["mistral-default"],
            },
        }
    },
    "qwen": {
        "models": {
            "qwen1.5-1.8b-chat": {
                "id": "Qwen/Qwen1.5-1.8B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-4b-chat": {
                "id": "Qwen/Qwen1.5-4B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-7b-chat": {
                "id": "Qwen/Qwen1.5-7B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-14b-chat": {
                "id": "Qwen/Qwen1.5-14B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-32b-chat": {
                "id": "Qwen/Qwen1.5-32B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-72b-chat": {
                "id": "Qwen/Qwen1.5-72B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen1.5-110b-chat": {
                "id": "Qwen/Qwen1.5-110B-Chat",
                "endpoints": ["together-default"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
            "qwen2-72b-instruct": {
                "id": "Qwen/Qwen2-72B-Instruct",
                "endpoints": ["siliconflow"],
                "function_call_available": False,
                "response_format_available": True,
                "context_length": 30000,
            },
        }
    },
    "yi": {
        "models": {
            "yi-large": {"id": "yi-large", "endpoints": ["lingyiwanwu-default"]},
            "yi-large-turbo": {"id": "yi-large-turbo", "endpoints": ["lingyiwanwu-default"]},
            "yi-large-fc": {"id": "yi-large-fc", "endpoints": ["lingyiwanwu-default"]},
            "yi-medium": {"id": "yi-medium", "endpoints": ["lingyiwanwu-default"]},
            "yi-medium-200k": {"id": "yi-medium-200k", "endpoints": ["lingyiwanwu-default"]},
            "yi-spark": {"id": "yi-spark", "endpoints": ["lingyiwanwu-default"]},
            "yi-vision": {"id": "yi-vision", "endpoints": ["lingyiwanwu-default"]},
        }
    },
    "zhipuai": {
        "models": {
            "glm-3-turbo": {"id": "glm-3-turbo", "endpoints": ["zhipuai-default"]},
            "glm-4": {"id": "glm-4", "endpoints": ["zhipuai-default"]},
            "glm-4-0520": {"id": "glm-4-0520", "endpoints": ["zhipuai-default"]},
            "glm-4-air": {"id": "glm-4-air", "endpoints": ["zhipuai-default"]},
            "glm-4-airx": {"id": "glm-4-airx", "endpoints": ["zhipuai-default"]},
            "glm-4-flash": {"id": "glm-4-flash", "endpoints": ["zhipuai-default"]},
            "glm-4-long": {"id": "glm-4-long", "endpoints": ["zhipuai-default"]},
            "glm-4v": {"id": "glm-4v", "endpoints": ["zhipuai-default"]},
        }
    },
}
