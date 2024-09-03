#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deeplx
# @Time         : 2024/3/1 16:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.translator_types import DeeplxRequest
from meutils.decorators.retry import retrying

from meutils.apis import niutrans


# niutrans.translate("你好", 'auto', 'en')

@alru_cache(ttl=3600)
@retrying()
async def translate(
        request: DeeplxRequest,
        api_key: Optional[str] = None,
):
    """
    https://fakeopen.org/DeepLX/#%E6%8E%A5%E5%8F%A3%E5%9C%B0%E5%9D%80
    https://linux.do/t/topic/111737
    """
    api_key = api_key or "FKZ9FqfYo43ogw99D9sHtW0qtiX2AvSiZjk0rBo5CdY"  # todo

    url = f"https://api.deeplx.org/{api_key}/translate"

    payload = request.model_dump()
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload)
            data = response.json()
            if not data.get('data'):
                raise Exception('DeeplxRequest error')
            else:
                return data
    except Exception as e:
        logger.error(e)
        _ = niutrans.translate(request.text, 'auto', request.target_lang.lower())
        return {'data': _}


if __name__ == '__main__':
    request = DeeplxRequest(text='火哥AI是最棒的', source_lang='ZH', target_lang='EN')
    with timer():
        arun(translate(request))
