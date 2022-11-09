import json
import httpx
import getopt
import base64
from nonebot import get_driver

from .config import Config
from .requests_json_generator import *

#获取配置
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']


async def text2img(msg):
    img2img_json = text2imgJSONGen(msg)

    #发送post请求生成绘图
    async with httpx.AsyncClient() as client:
        response = await client.post(url=base_url+'/sdapi/v1/txt2img',data=img2img_json, timeout=60)
        print(response)
    
    #解码图片
    img_list = [base64.b64decode(i) for i in response.json()['images']]
    return img_list