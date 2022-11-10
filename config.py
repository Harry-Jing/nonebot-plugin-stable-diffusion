from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    aidraw_base_url:str = "http://127.0.0.1:7860"
    
    aidraw_default_prompt:str = "masterpiece, best quality, "
    aidraw_default_negative_prompt:str = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, \
extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, \
watermark, username, blurry, bad feet, bad eyes"
    aidraw_default_step:int = 28
    aidraw_default_scale:int = 12
    aidaidraw_default_width: int = 576
    aidaidraw_default_height: int = 768

    aidraw_max_count:int = 4
    

