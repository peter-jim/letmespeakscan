import time
# 使用协程
import asyncio
import aiohttp


async def getPage(url):  # 定义了一个协程对象，python中函数也是对象
    print("开始爬取网站", url)
    time.sleep(4)  # 阻塞
    print("爬取完成！！！", url)


# async修饰的函数返回的对象
c = getPage(11)

# 创建事件对象
loop_event = asyncio.get_event_loop()
# 注册并启动looP
loop_event.run_until_complete(c)

# task对象使用，封装协程对象c
'''
loop_event = asyncio.get_event_loop()
task = loop_event.create_task(c)
loop_event.run_until_complete(task)
'''

# Future对象使用，封装协程对象c            用法和task差不多
'''
loop_event = asyncio.get_event_loop()
task       = asyncio.ensure_future(c)
loop_event.run_until_complete(task)
'''


# 绑定回调使用

async def getPage2(url):  # 定义了一个协程对象，python中函数也是对象
    print("开始爬取网站", url)
    time.sleep(2)  # 阻塞
    print("爬取完成！！！", url)
    return url


# async修饰的函数返回的对象
c2 = getPage2(2)


def callback_func(task):
    print(task.result())  # task.result()返回任务对象中封装的协程对象对应函数的返回值


# 绑定回调
loop_event = asyncio.get_event_loop()
task = asyncio.ensure_future(c2)

task.add_done_callback(callback_func)  # 真正绑定，
loop_event.run_until_complete(task)
