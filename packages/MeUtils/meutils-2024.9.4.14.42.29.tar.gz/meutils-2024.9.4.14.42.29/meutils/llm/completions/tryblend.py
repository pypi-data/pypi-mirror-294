#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tryblend
# @Time         : 2024/9/4 09:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.schemas.tryblend_types import BASE_URL, FEISHU_URL, create_request

from meutils.pipe import *
from meutils.notice.feishu import send_message as _send_message
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling

from meutils.llm.openai_utils import to_openai_completion_params, token_encoder, token_encoder_with_cache
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage
from openai import OpenAI, AsyncOpenAI, APIStatusError

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: ChatCompletionRequest):
        token = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL)

        payload = create_request(request.messages, request.model)
        headers = {
            'Cookie': token,
            'next-action': 'ca5ce500ddee37bddc3c986bee81b599f41e3efb',

        }

        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
            async with client.stream(method="POST", url="", json=payload) as response:
                async for chunk in response.aiter_lines():
                    if chunk and (chunk := chunk.split(":", maxsplit=1)[1]).strip() and chunk.startswith("{"):
                        try:
                            chunk = json.loads(chunk)
                            chunk = chunk.get('diff', [""])[-1] or chunk.get('curr', "")
                            yield chunk

                        except Exception as e:
                            _ = f"{e}\n{chunk}"
                            logger.error(_)
                            send_message(_)


if __name__ == '__main__':
    token = '_gcl_au=1.1.1117087196.1725410224.1885527058.1725410233.1725410233; session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoiY2hhdGZpcmVAcXEuY29tIn0sImV4cGlyZXMiOiIyMDI0LTEyLTEzVDAwOjM4OjAzLjg3NVoiLCJpYXQiOjE3MjU0MTAyODMsImV4cCI6MTczNDA1MDI4M30.ezlumcBmuARnLoEFcwQCe5JqYZSZRUqN09AyxZvCbm0'
    token = None
    c = Completions(token)
    request = ChatCompletionRequest(
        model="perplexity",
        messages=[{'role': 'user', 'content': '南京天气怎么样'}]
    )


    async def main():
        async for i in c.create(request):
            print(i, end='')


    arun(main())
