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
        await shell_command_draw.finish(parser.format_help())
    if argv == []:
        #无内容 -> 发送帮助
        await shell_command_draw.finish(parser.format_help())

    #获取数据至data
    d = {key:value for key,value in vars(args).items() if value!=None}
    prompt = ''.join(d.pop('prompt', ''))
    negaive_prompt = ''.join(d.pop('negaive_prompt', ''))
    try:
        data = GeneralText2imgData(prompt = prompt,negative_prompt = negaive_prompt, **d)
    except ValidationError:
        await shell_command_draw.finish(parser.format_help())
    
    #获取图片
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