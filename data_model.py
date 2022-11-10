from pydantic import BaseModel, ValidationError, validator

from nonebot import get_driver
from .config import Config

plugin_config = Config.parse_obj(get_driver().config).dict()

class Text2imgData(BaseModel):
    prompt: str
    negative_prompt: str
    count: int = 1
    step: int = plugin_config['aidraw_default_step']
    width: int = plugin_config['aidaidraw_default_width']
    height: int = plugin_config['aidaidraw_default_height']
    scale: float = plugin_config['aidraw_default_scale']

    @validator('prompt')
    def add_default_prompt(cls, value):
        return plugin_config['aidraw_default_prompt'] + value

    @validator('negative_prompt')
    def add_default_negative_prompt(cls, value):
        return plugin_config['aidraw_default_negative_prompt'] + value

    @validator('count', 'step', 'width', 'height', 'scale')
    def value_must_be_positive(cls, value):
        if not value > 0:
            raise ValueError
        return value

    @validator('width', 'height')
    def resolution_must_be_multiple_of_64(cls, value):
        if not value%64 == 0:
            return round(value//64)*64
        return value



class SD_webui_Text2imgData(BaseModel):
    enable_hr  =  false
    denoising_strength  =  0
    firstphase_width  =  0
    firstphase_height  =  0
    prompt  = ''
    styles  =  ['string']
    seed  =  -1
    subseed  =  -1
    subseed_strength  =  0
    seed_resize_from_h  =  -1
    seed_resize_from_w  =  -1
    batch_size  =  1
    n_iter  =  1
    steps  =  50
    cfg_scale  =  7
    width  =  512
    height  =  512
    restore_faces  =  false
    tiling  =  false
    negative_prompt  =  string
    eta  =  0
    s_churn  =  0
    s_tmax  =  0
    s_tmin  =  0
    s_noise  =  1
    sampler_index  =  Euler