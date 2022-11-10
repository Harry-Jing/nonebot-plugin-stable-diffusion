from pydantic import BaseModel, validator

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
    scale: int = plugin_config['aidraw_default_scale']

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
    