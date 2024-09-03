#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task_types
# @Time         : 2024/5/31 15:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from enum import Enum

from meutils.pipe import *


class TaskType(str, Enum):
    # 存储
    oss = "oss"

    # 百度助手
    pcedit = "pcedit"

    # 图 音频 视频

    kling = "kling"
    kling_vip = "kling@vip"

    vidu = "vidu"
    vidu_vip = "vidu@vip"

    suno = "suno"
    haimian = "haimian"
    lyrics = "lyrics"

    runwayml = "runwayml"
    fish = 'fish'
    cogvideox = "cogvideox"

    faceswap = "faceswap"

    # 文档智能
    file_extract = "file-extract"
    moonshot_fileparser = "moonshot-fileparser"
    textin_fileparser = "textin-fileparser"

    # 语音克隆 tts  Voice clone
    tts = "tts"
    voice_clone = "voice-clone"

    # todo
    assistants = "assistants"
    fine_tune = "fine-tune"


Purpose = TaskType


class Task(BaseModel):
    id: Union[str, int] = Field(default_factory=lambda: shortuuid.random())
    status: Union[str, int] = "success"  # pending, running, success, failed

    status_code: Optional[int] = None

    data: Optional[Any] = None
    metadata: Optional[Any] = None
    # metadata: Optional[Dict[str, str]] = None
    description: Optional[str] = None

    system_fingerprint: Optional[str] = None  # api-key token cookie 加密

    created_at: int = Field(default_factory=lambda: int(time.time()))


class FileTask(BaseModel):
    id: Union[str, int] = Field(default_factory=lambda: shortuuid.random())
    status: Optional[str] = None  # pending, running, success, failed
    status_code: Optional[int] = None

    data: Optional[Any] = None
    metadata: Optional[Any] = None

    system_fingerprint: Optional[str] = None  # api-key token cookie 加密

    created_at: int = Field(default_factory=lambda: int(time.time()))

    url: Optional[str] = None


# pass

if __name__ == '__main__':
    # print(TaskType("kling").name)
    #
    # print(TaskType("kling") == 'kling')

    # print(Task(id=1, status='failed', system_fingerprint='xxx').model_dump(exclude={"system_fingerprint"}))

    # print("kling" == TaskType.kling)
    # print("kling" == Purpose.kling)

    # print(Purpose('kling').value)
    # print(Purpose.vidu.startswith('vidu'))

    # print('vidu' in Purpose.vidu)

    # print('kling_vip' in {TaskType.kling, TaskType.kling_vip})

    # print('kling_vip'.startswith(TaskType.kling))

    print(Purpose.__members__)
    print(list(Purpose))
