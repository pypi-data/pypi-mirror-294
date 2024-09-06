#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tryblend_types
# @Time         : 2024/9/4 08:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://www.tryblend.ai/"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=hxVlQw"


def create_request(messages, model="perplexity"):
    request = None
    if model.startswith(("perplexity", "net")):
        request = [
            {
                "requestId": "33020359-a99e-4fdd-a170-58a3be351f11",
                "selectedModel": {
                    "id": "perplexity/llama-3.1-sonar-small-128k-online",
                    "active": True,
                    "name": "Perplexity Sonar Small",
                    "provider": "perplexity",
                    "maker": "perplexity",
                    "makerHumanName": "Perplexity",
                    "fallbackIcon": None,
                    "providerModelId": "llama-3.1-sonar-small-128k-online",
                    "info": {
                        "description": "The smaller, internet-connected chat model by Perplexity Labs, based on Llama 3.1. The online models are focused on delivering helpful, up-to-date, and factual responses.",
                        "fundationModel": "LLama 3 8B",
                        "fundationModelMaker": "Meta",
                        "releaseDate": "August 2024",
                        "knowledgeCutoff": "Today",
                        "context": "128000",
                        "predictionTimeSecond": None,
                        "usableAsAssistant": False,
                        "pricing": {
                            "inputImagePrice": None,
                            "inputPrice": 0.2,
                            "outputPrice": 0.2,
                            "inputPriceUnit": "request",
                            "outputPriceUnit": "1m tokens"
                        },
                        "inputType": [
                            "text"
                        ],
                        "outputType": [
                            "text"
                        ],
                        "type": [
                            "text"
                        ],
                        "keywords": [
                            "free",
                            "online search"
                        ],
                        "website": "https://blog.perplexity.ai/blog/introducing-pplx-online-llms",
                        "fallbackModel": None
                    },
                    "parameters": [
                        {
                            "name": "prompt",
                            "description": "The prompt to use for the request",
                            "parameterType": "directInput",
                            "defaultValue": ""
                        },
                        {
                            "name": "file",
                            "description": "Files to use as complimentary information for the prompt.",
                            "parameterType": "directInput",
                            "defaultValue": [],
                            "fileOptions": [
                                {
                                    "fileExtension": [
                                        ".c",
                                        ".cpp",
                                        ".cs",
                                        ".java",
                                        ".py",
                                        ".rb",
                                        ".js",
                                        ".ts",
                                        ".tsx",
                                        ".jsx",
                                        ".php",
                                        ".go",
                                        ".swift",
                                        ".kt",
                                        ".scala",
                                        ".rs",
                                        ".lua",
                                        ".pl",
                                        ".sh",
                                        ".bash",
                                        ".ps1",
                                        ".html",
                                        ".css",
                                        ".scss",
                                        ".less",
                                        ".json",
                                        ".xml",
                                        ".yaml",
                                        ".yml",
                                        ".md",
                                        ".markdown",
                                        ".txt",
                                        ".rtf",
                                        ".tex",
                                        ".log",
                                        ".xlsx",
                                        ".pdf",
                                        ".csv",
                                        ".tsv",
                                        ".ini",
                                        ".cfg",
                                        ".conf",
                                        ".toml",
                                        ".sql",
                                        ".r",
                                        ".m",
                                        ".f",
                                        ".f90",
                                        ".vb",
                                        ".bas",
                                        ".ps",
                                        ".asm"
                                    ],
                                    "fileExtensionName": "text",
                                    "maxFileSize": 5,
                                    "minFileCount": 0,
                                    "maxFileCount": 10
                                }
                            ]
                        }
                    ]
                },
                "messages": messages,
                "sessionId": "3295a8cd-e458-4993-8ad7-4d24e20103fe",
                "userMessageId": "22fbe79f-9e65-4095-98ee-fca275a4d88d",
                "assistantMessageId": "04898f12-0826-4eb1-be32-9c3dfbf24732"
            }
        ]
    elif model == "claude-3-haiku":
        request = [
            {
                "requestId": "08c62f1c-3945-4b3c-ae78-4e0925885870",
                "selectedModel": {
                    "id": "openrouter:anthropic/claude-3-haiku",
                    "active": True,
                    "name": "Claude 3 Haiku",
                    "provider": "openrouter",
                    "maker": "anthropic",
                    "makerHumanName": "Anthropic",
                    "fallbackIcon": None,
                    "providerModelId": "anthropic/claude-3-haiku",
                    "info": {
                        "description": "Claude 3 Haiku is Anthropic's fastest and most compact model for near-instant responsiveness. Quick and accurate targeted performance.",
                        "fundationModel": None,
                        "fundationModelMaker": None,
                        "releaseDate": "March 4, 2024",
                        "knowledgeCutoff": None,
                        "context": "200000",
                        "predictionTimeSecond": None,
                        "usableAsAssistant": False,
                        "pricing": {
                            "inputImagePrice": 0.0004,
                            "inputPrice": 0.25,
                            "outputPrice": 1.25,
                            "inputPriceUnit": "1m tokens",
                            "outputPriceUnit": "1m tokens"
                        },
                        "inputType": [
                            "text",
                            "image"
                        ],
                        "outputType": [
                            "text"
                        ],
                        "type": [
                            "text",
                            "vision"
                        ],
                        "keywords": [
                            "free",
                            "vision"
                        ],
                        "website": "https://www.anthropic.com/news/claude-3-family",
                        "fallbackModel": None
                    },
                    "parameters": [
                        {
                            "name": "prompt",
                            "description": "The prompt to use for the request",
                            "parameterType": "directInput",
                            "defaultValue": ""
                        },
                        {
                            "name": "file",
                            "description": "Files to use as complimentary information for the prompt.",
                            "parameterType": "directInput",
                            "defaultValue": [],
                            "fileOptions": [
                                {
                                    "fileExtension": [
                                        ".jpg",
                                        ".jpeg",
                                        ".webp",
                                        ".png",
                                        ".gif"
                                    ],
                                    "fileExtensionName": "image",
                                    "maxFileSize": 5,
                                    "minFileCount": 0,
                                    "maxFileCount": 20
                                },
                                {
                                    "fileExtension": [
                                        ".c",
                                        ".cpp",
                                        ".cs",
                                        ".java",
                                        ".py",
                                        ".rb",
                                        ".js",
                                        ".ts",
                                        ".tsx",
                                        ".jsx",
                                        ".php",
                                        ".go",
                                        ".swift",
                                        ".kt",
                                        ".scala",
                                        ".rs",
                                        ".lua",
                                        ".pl",
                                        ".sh",
                                        ".bash",
                                        ".ps1",
                                        ".html",
                                        ".css",
                                        ".scss",
                                        ".less",
                                        ".json",
                                        ".xml",
                                        ".yaml",
                                        ".yml",
                                        ".md",
                                        ".markdown",
                                        ".txt",
                                        ".rtf",
                                        ".tex",
                                        ".log",
                                        ".xlsx",
                                        ".pdf",
                                        ".csv",
                                        ".tsv",
                                        ".ini",
                                        ".cfg",
                                        ".conf",
                                        ".toml",
                                        ".sql",
                                        ".r",
                                        ".m",
                                        ".f",
                                        ".f90",
                                        ".vb",
                                        ".bas",
                                        ".ps",
                                        ".asm"
                                    ],
                                    "fileExtensionName": "text",
                                    "maxFileSize": 5,
                                    "minFileCount": 0,
                                    "maxFileCount": 10
                                }
                            ]
                        }
                    ]
                },
                "messages": messages,
                "sessionId": "013bded3-3897-44ee-b658-54fa9cf97ab4",
                "userMessageId": "4fca60c2-bbdb-4f98-9de8-8b8c8bf9a908",
                "assistantMessageId": "ae2962d5-c9a0-410b-8f06-79eb59bb3119"
            }
        ]

    else:
        # elif model == "gpt-4o-mini":
        request = [
            {
                "requestId": "f61da86c-10c7-46e3-86fe-484d86577b59",
                "selectedModel": {
                    "id": "openai:gpt-4o-mini",
                    "active": True,
                    "name": "GPT 4o Mini",
                    "provider": "openai",
                    "maker": "openai",
                    "makerHumanName": "OpenAI",
                    "fallbackIcon": None,
                    "providerModelId": "gpt-4o-mini",
                    "info": {
                        "description": "GPT-4o mini is OpenAI's most cost-efficient small model that’s smarter and cheaper than GPT-3.5 Turbo, and has vision capabilities.",
                        "fundationModel": "GPT-4",
                        "fundationModelMaker": "OpenAI",
                        "releaseDate": "2024",
                        "knowledgeCutoff": "October, 2023",
                        "context": "128000",
                        "predictionTimeSecond": None,
                        "usableAsAssistant": True,
                        "pricing": {
                            "inputImagePrice": 0.003,
                            "inputPrice": 0.15,
                            "outputPrice": 0.6,
                            "inputPriceUnit": "1m tokens",
                            "outputPriceUnit": "1m tokens"
                        },
                        "inputType": [
                            "text",
                            "image"
                        ],
                        "outputType": [
                            "text"
                        ],
                        "type": [
                            "text",
                            "vision"
                        ],
                        "keywords": [
                            "free",
                            "vision"
                        ],
                        "website": "https://openai.com/research/gpt-4",
                        "fallbackModel": None
                    },
                    "parameters": [
                        {
                            "name": "prompt",
                            "description": "The prompt to use for the request",
                            "parameterType": "directInput",
                            "defaultValue": ""
                        },
                        {
                            "name": "file",
                            "description": "Files to use as complimentary information for the prompt.",
                            "parameterType": "directInput",
                            "defaultValue": [],
                            "fileOptions": [
                                {
                                    "fileExtension": [
                                        ".jpg",
                                        ".jpeg",
                                        ".webp",
                                        ".png",
                                        ".gif"
                                    ],
                                    "fileExtensionName": "image",
                                    "maxFileSize": 5,
                                    "minFileCount": 0,
                                    "maxFileCount": 20
                                },
                                {
                                    "fileExtension": [
                                        ".c",
                                        ".cpp",
                                        ".cs",
                                        ".java",
                                        ".py",
                                        ".rb",
                                        ".js",
                                        ".ts",
                                        ".tsx",
                                        ".jsx",
                                        ".php",
                                        ".go",
                                        ".swift",
                                        ".kt",
                                        ".scala",
                                        ".rs",
                                        ".lua",
                                        ".pl",
                                        ".sh",
                                        ".bash",
                                        ".ps1",
                                        ".html",
                                        ".css",
                                        ".scss",
                                        ".less",
                                        ".json",
                                        ".xml",
                                        ".yaml",
                                        ".yml",
                                        ".md",
                                        ".markdown",
                                        ".txt",
                                        ".rtf",
                                        ".tex",
                                        ".log",
                                        ".xlsx",
                                        ".pdf",
                                        ".csv",
                                        ".tsv",
                                        ".ini",
                                        ".cfg",
                                        ".conf",
                                        ".toml",
                                        ".sql",
                                        ".r",
                                        ".m",
                                        ".f",
                                        ".f90",
                                        ".vb",
                                        ".bas",
                                        ".ps",
                                        ".asm"
                                    ],
                                    "fileExtensionName": "text",
                                    "maxFileSize": 5,
                                    "minFileCount": 0,
                                    "maxFileCount": 10
                                }
                            ]
                        }
                    ]
                },
                "messages": messages,
                "sessionId": "dcb21600-8767-4a18-863e-ecead15e1b87",
                "userMessageId": "20ca590e-c76b-4790-b298-4350bde4ee83",
                "assistantMessageId": "6c1ba298-b24c-4ba5-b7f8-09769793b399"
            }
        ]

    return request


if __name__ == '__main__':
    import json_repair

    print("net".startswith(("perplexity", "net")))
