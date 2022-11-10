from typing import Union

from nonebot import Bot
from nonebot.log import logger
from nonebot.rule import ArgumentParser, Namespace
#from nonebot.adapters import Message, MessageSegment, MessageTemplate
from nonebot.params import ShellCommandArgv, ShellCommandArgs
from nonebot.plugin.on import on_shell_command
from nonebot.exception import ParserExit

from .data_model import *

parser = ArgumentParser()
parser.add_argument('--count')
parser.add_argument('--step')
parser.add_argument('--resolution')
parser.add_argument('--scale')
parser.add_argument('prompt',nargs='*')


shell_command_draw = on_shell_command("绘图", parser=parser)

@shell_command_draw.handle()
async def test(bot:Bot, argv:list = ShellCommandArgv(), args:Union[Namespace,ParserExit] = ShellCommandArgs()):
    if isinstance(args, ParserExit):
        #错误输入
        await shell_command_draw.finish(f'ParserExit: {args.status=}')
    if argv == []:
        #无内容 -> 发送帮助
        await shell_command_draw.send(f'argv=[]')
        await shell_command_draw.finish(parser.format_help())
    
    d = {key:value for key,value in vars(args).items() if value!=None}
    prompt = ''.join(d.pop('prompt', ''))
    negaive_prompt = ''.join(d.pop('negaive_prompt', ''))
    shell_command_draw.send(f'{d=}')
    try:
        data = Text2imgData(prompt = prompt,negative_prompt = negaive_prompt, **d)
    except ValidationError:
        await shell_command_draw.finish(parser.format_help())

    await shell_command_draw.send(f'{data=}')