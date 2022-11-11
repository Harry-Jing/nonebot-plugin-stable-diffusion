from nonebot.rule import ArgumentParser

help_content = '''AI 画图
用法：
    #绘图 [--count <count>] [--step <step>] [--resolution <width>x<height>] [--scale <scale>] prompt 

    输入用逗号隔开的英文标签，例如：#绘图 loli, school uniform, smile

可用的选项：
    -h, --help    显示帮助信息
    --count <count>    画图数量
    --step <step>    采样步数，大于40后不会有明显进步
    --resolution <width>x<height>    更改分辨率
    --scale <scale>    调整服从标签的强度

这个项目是自己搞着玩的
项目地址：https://github.com/Harry-Jing/nonebot-plugin-stable-diffusion'''

parser = ArgumentParser()
parser.add_argument('--count')
parser.add_argument('--step')
parser.add_argument('--resolution')
parser.add_argument('--scale')
parser.add_argument('prompt',nargs='*')

