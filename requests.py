import httpx
import base64
from nonebot import get_driver

#获取配置
from .config import Config
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']


async def SDWebuiText2imgRequest(json_data):

    #发送post请求生成绘图
    async with httpx.AsyncClient() as client:
        response = await client.post(url=base_url+'/sdapi/v1/txt2img',data=json_data, timeout=60)
        print(response)
    
    #解码图片
    img_list = [base64.b64decode(i) for i in response.json()['images']]
    return img_list