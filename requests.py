import httpx
import base64
from typing import Tuple
from nonebot import get_driver

#获取配置
from .config import Config
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']


async def SDWebuiText2imgRequest(request_json) -> Tuple[list[bytes], str]:

    #发送post请求生成绘图
    async with httpx.AsyncClient() as client:
        response = await client.post(url=base_url+'/sdapi/v1/txt2img',data=request_json, timeout=60)
        print(response)
    
    #解码图片
    response_json = response.json()
    print(response_json)
    img_list = [base64.b64decode(i) for i in response_json['images']]
    info = response_json['info']
    print(info)
    return img_list, info