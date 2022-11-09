import json
import getopt
from nonebot import get_driver
from .config import Config
#获取配置
plugin_config = Config.parse_obj(get_driver().config).dict()
base_url = plugin_config['aidraw_base_url']
default_promp = plugin_config['aidraw_default_prompt']
default_negative_promp = plugin_config['aidraw_default_negative_prompt']

def text2imgJSONGen(msg):
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
                requests_dict['width']= width
                requests_dict['height']= height

    img2img_json = json.dumps(requests_dict)
    
    print(f'{img2img_json=}')
    
    return img2img_json