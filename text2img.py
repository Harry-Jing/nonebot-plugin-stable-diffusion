import json
from msilib.schema import Error
import httpx
import getopt
import base64
from copy import deepcopy
from nonebot import get_driver
from .config import Config
from .getIMG import getIMG
#获取配置
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']
default_promp = plugin_config['aidraw_default_prompt']
default_negative_promp = plugin_config['aidraw_default_negative_prompt']


async def text2img(msg):
    #处理输入参数
    opts, data = getopt.getopt(msg.split(), '',['step=','scale=','resolution=','count='])
    print(f'{opts=}, {data=}')
    opt_dict = {key:value for key, value in opts}
    prompt = ' '.join(data)

    #配置请求json
    requests_dict = dict()
    requests_dict['prompt'] = default_promp + prompt
    requests_dict['negative_promp'] = default_negative_promp
    for opt in opts:
        match opt[0]:
            case '--step':
                print(f'step={opt[1]}')
                requests_dict['steps']= int(opt[1])
            case '--count':
                print(f'count={opt[1]}')
                requests_dict['n_iter']= int(opt[1])
            case '--scale':
                print(f'scale={opt[1]}')
                requests_dict['cfg_scale'] = int(opt[1])
            case '--resolution':
                print(f'resolution={opt[1]}')
                width, height = (int(i) for i in opt[1].split('x'))
                if not (width%64==0 and height%64==0):
                    print("wrong resolution")
                    raise Error
                requests_dict['width']= width
                requests_dict['height']= height

    img2img_json = json.dumps(requests_dict)
    
    print(f'{img2img_json=}')

    #发送post请求生成绘图
    async with httpx.AsyncClient() as client:
        response = await client.post(url=base_url+'/sdapi/v1/txt2img',data=img2img_json, timeout=60)
        print(response)
    
    #发送get请求下载绘图
    img_list = [base64.b64decode(i) for i in response.json()['images']]
    return img_list