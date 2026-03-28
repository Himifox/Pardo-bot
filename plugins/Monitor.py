from nonebot import require, get_bot
from datetime import datetime, timedelta

# 引入定时任务插件
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

# 记录最后一次消息的时间
last_active_time = datetime.now()

# 假设的一个阈值：10分钟不说话就触发
SILENCE_THRESHOLD = timedelta(minutes=10)

@scheduler.scheduled_job("interval", minutes=1, id="check_silence")
async def check_silence():
    global last_active_time
    now = datetime.now()
    
    if now - last_active_time > SILENCE_THRESHOLD:
        # 触发主动找话题逻辑
        bot = get_bot()
        # 这里需要逻辑去调用 LLM，询问：
        # “现在冷场了，请使用 proactive_topic 动作为你的观众找个话题。”
        
        # 成功触发后，重置时间防止刷屏
        last_active_time = now