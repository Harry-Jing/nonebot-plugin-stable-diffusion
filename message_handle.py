from typing import Union

from nonebot import Bot
from nonebot.log import logger
from nonebot.rule import ArgumentParser, Namespace
from nonebot.params import ShellCommandArgv, ShellCommandArgs
from nonebot.plugin.on import on_shell_command
from nonebot.exception import ParserExit
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, MessageSegment

from .requests import *
from .data_model import *

help_content = '''AI 画图
用法：
    #绘图 [--count <count>] [--step <step>] [--resolution <width>x<height>] [--scale <scale>] prompt 

    输入用逗号隔开的英文标签，例如：#绘图 loli, school uniform, smile

可用的选项：
    -h, --help    显示帮助信息
    --count <count>    画图数量
    --step <step>    采样部署，大于40后不会有明显进步
    --resolution <width>x<height>    更爱分辨率
    --scale <scale>    更改CFG Scale，调整服从标签的强度

这个项目是自己搞着玩的
项目地址：https://github.com/Harry-Jing/nonebot-plugin-stable-diffusion'''

parser = ArgumentParser()
parser.add_argument('--count')
parser.add_argument('--step')
parser.add_argument('--resolution')
parser.add_argument('--scale')
parser.add_argument('prompt',nargs='*')


shell_command_draw = on_shell_command("绘图", parser=parser)

@shell_command_draw.handle()
async def test(bot:Bot, event:MessageEvent, argv:list = ShellCommandArgv(), args:Union[Namespace,ParserExit] = ShellCommandArgs()):
    #处理发送数据
    if isinstance(args, ParserExit):
        #错误输入
        await shell_command_draw.send('错误输入')
        await shell_command_draw.finish(help_content)
    if argv == []:
        #无内容 -> 发送帮助
        await shell_command_draw.finish(help_content)

    #获取数据至data
    try:
        input_args_dict = vars(args)
        print(input_args_dict)
        if not input_args_dict['resolution'] == None:
            input_args_dict['width'], input_args_dict['height'] = input_args_dict.pop('resolution')
        prompt = ''.join(input_args_dict.pop('prompt', ''))
        negaive_prompt = ''.join(input_args_dict.pop('negaive_prompt', ''))
        data_dict = {key:value for key,value in input_args_dict.items() if value!=None}
        data = GeneralText2imgData(prompt = prompt,negative_prompt = negaive_prompt, **data_dict)
    except:
        await shell_command_draw.send('格式错误')
        await shell_command_draw.finish(help_content)
    #获取图片
    await shell_command_draw.send('开始画了，别急')
    img_list, info = await SDWebuiText2imgRequest(GeneralText2imgData_to_SDWebuiText2imgData(data).json())
    #发送图片
    message = [MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=MessageSegment.text(info)
                )]
    for img in img_list:
        message.append(MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=MessageSegment.image(img)
                ))
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=message)
    else:
        await bot.send_private_forward_msg(user_id=event.user_id, messages=message)