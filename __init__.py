from nonebot import Bot
from nonebot import get_driver
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command,on_message
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, MessageSegment

from .config import Config
from .img2img import img2img


message_draw = on_command("绘图")

@message_draw.handle()
async def draw(bot:Bot, event:MessageEvent, args:Message = CommandArg() ):
    print(args.extract_plain_text())
    try:
        pass
    except:
        await bot.send(event=event, message='请求出错')
        
    img_list = await img2img(args.extract_plain_text())
    message = [MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=MessageSegment.text(args.extract_plain_text())
                )]
    for img in img_list:
        message.append(MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=MessageSegment.image(img.content)
                ))
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=message)
    else:
        await bot.send_private_forward_msg(user_id=event.user_id, messages=message)

    '''
    message =  MessageSegment.reply(event.message_id)
    for img in img_list:
        message += MessageSegment.image(img.content)
    await bot.send(event=event, message=message)'''

message_draw = on_command("测试")

@message_draw.handle()
async def draw(bot:Bot, event:MessageEvent, args:Message = CommandArg()):
    #msg = MessageSegment.node_custom(user_id=508069996, nickname="123", content="abc")

    #msg = MessageSegment("node", {"user_id":508069996, "nickname":"123", "content":"abc"}) +\
    #MessageSegment("node", {"user_id":508069996, "nickname":"123", "content":"abc"})
    msg_1 = MessageSegment.node_custom(
                user_id=event.user_id,
                nickname="AI画家",
                content=Message("Test"),
            )
    msg = [msg_1,msg_1,msg_1]
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg)
    else:
        await bot.send_private_forward_msg(user_id=event.user_id, messages=msg)
