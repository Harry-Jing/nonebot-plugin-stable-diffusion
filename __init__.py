from httpx import HTTPError, TimeoutException

from nonebot import Bot
from nonebot import get_driver
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command

from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, MessageSegment

from .config import Config
from .text2img import text2img


message_draw = on_command("绘图")

@message_draw.handle()
async def draw(bot:Bot, event:MessageEvent, args:Message = CommandArg()):
    await bot.send(event=event, message='在画了，别急')
    print(args.extract_plain_text())

    try:
        img_list = await text2img(args.extract_plain_text())
    except TimeoutException:
        await bot.send(event=event, message='请求超时')
    except HTTPError:
        await bot.send(event=event, message='其他网络错误')
        
    message = [MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=MessageSegment.text(args.extract_plain_text())
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