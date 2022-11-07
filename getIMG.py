import httpx
from nonebot import get_driver
from .config import Config

#获取配置
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']


async def getIMG(file_name_list:list):
    img_list = []
    for file_name in file_name_list:
        async with httpx.AsyncClient() as client:
            img = await client.get(url=base_url+'/file='+file_name, timeout=60)
            img_list.append(img)
    
    return img_list