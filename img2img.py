import json
from msilib.schema import Error
import httpx
import getopt
from copy import deepcopy
from nonebot import get_driver
from .config import Config
from .getIMG import getIMG
#获取配置
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']
default_promp = plugin_config['aidraw_default_prompt']
default_negative_promp = plugin_config['aidraw_default_negative_prompt']

with open("./src/plugins/nonebot-plugin-stable-diffusion/default_json/img2img.json", encoding="utf-8") as f:
        img2img_default_dict:dict = json.loads(f.read())



async def img2img(msg):
    #处理输入参数
    opts, data = getopt.getopt(msg.split(), '',['step=','scale=','resolution=','count='])
    print(f'{opts=}, {data=}')
    opt_dict = {key:value for key, value in opts}
    prompt = ' '.join(data)

    #配置请求json
    img2img_dict = deepcopy(img2img_default_dict)
    img2img_dict['data'][0] = default_promp + prompt
    img2img_dict['data'][1] = default_negative_promp
    for opt in opts:
        match opt[0]:
            case '--step':
                print(f'step={opt[1]}')
                img2img_dict['data'][4] = int(opt[1])
            case '--count':
                print(f'count={opt[1]}')
                img2img_dict['data'][8] = int(opt[1])
            case '--scale':
                print(f'scale={opt[1]}')
                img2img_dict['data'][10] = int(opt[1])
            case '--resolution':
                print(f'resolution={opt[1]}')
                width, height = (int(i) for i in opt[1].split('x'))
                if not (width%64==0 and height%64==0):
                    print("wrong resolution")
                    raise Error
                img2img_dict['data'][17] = height
                img2img_dict['data'][18] = width
                print(1)

    img2img_json = json.dumps(img2img_dict)
    
    print(f'{img2img_json=}')

    #发送post请求生成绘图
    async with httpx.AsyncClient() as client:
        response = await client.post(url=base_url+'/api/predict/',data=img2img_json, timeout=60)
        print(response)
    
    #发送get请求下载绘图
    file_name_list = [i['name'] for i in response.json()['data'][0]]
    img_list = await getIMG(file_name_list)
    return img_list