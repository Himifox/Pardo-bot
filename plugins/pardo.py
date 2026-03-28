from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
import asyncio
import httpx
import os
import base64
from typing import Optional, Dict
import logging
import base64
import json
import re
import random
import httpx
import os
import time
import logging
from typing import Optional, Dict, List
from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot
from nonebot.exception import FinishedException
from openai import AsyncOpenAI

from plugins.memory import get_history_str, save_bot_reply
from .import Sticker_sender
from plugins.Sticker_recognize import smart_send
from plugins.config import *
# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# 
# ===========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def to_api_path(rel_path: str) -> str:
    """解决 API 找不到文件的核心：转为绝对路径且强制使用正斜杠"""
    abs_path = os.path.join(BASE_DIR, rel_path)
    return abs_path.replace("\\", "/")

# ================= 配置区域 =================
SOVITS_API_URL = "http://127.0.0.1:9880/tts"
REFER_WAV_PATH = to_api_path("ref_audio/罐头.wav")  # 建议换成帕朵的参考音频
PROMPT_TEXT = "罐头，你怎么才回来……嗯？找到了个开店的好地方？在哪在哪？"  # 对应参考音频的文字
AUX_PATH_1 = "ref_audio/罐头，你怎么才回来……嗯？找到了个开店的好地方？在哪在哪？.wav"
AUX_PATH_2 = "ref_audio/喵喵喵 喵喵喵 喵喵喵.wav"
aux_ref_audio_paths = [AUX_PATH_1, AUX_PATH_2]
PROMPT_LANG = "zh"
# 参考音频目录与关键词映射（可在此手动添加显式映射）
REF_AUDIO_DIR = "ref_audio"
REF_KEYWORD_MAP: Dict[str, str] = {}
# 缓存配置：避免每次请求都扫描目录
REF_MAP_CACHE: Optional[Dict[str, str]] = None
REF_MAP_CACHE_TIME: float = 0
# 缓存过期时间（秒）
REF_MAP_TTL = 300

API_KEY = "sk-156ebc486b924ebc8b94656f4a3cfa86"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"
HISTORY_FILE_PATH = "MSG/group_712851492_20260203_231902.json"

ADMIN_UID = "3461737415"  # 你的纯数字 UID
TARGET_UID = "u_MkWCKLdJG7Jubt9cQXbSpg"  # 语料学习目标 UID
ACTIVATE_COMMAND = "#Neko"  # 激活指令
WHITE_LIST_FILE = "active_groups.json"

TEXT_PROBABILITY = 0.9
VOICE_PROBABILITY = 0.5
GLOBAL_CD = 30  # 全局冷却时间，单位秒
VOICE_KEYWORDS = [ "语音", "声音", "唱歌", "听听", "想你了帕朵"]
TXT_KEYWORDS = ["帕朵"]
last_reply_time = {}

driver = get_driver()
async def get_sovits_audio(text: str, ref_path: Optional[str] = None) -> Optional[str]:
    try:
        target_ref = to_api_path(ref_path) if ref_path else REFER_WAV_PATH
        # 物理检查：如果文件真的不在，直接拦截并报错
        if not os.path.exists(target_ref):
            logger.error(f"❌ 物理路径不存在，请检查文件: {target_ref}")
            return None

        async with httpx.AsyncClient(timeout=160.0, trust_env=False) as http_client:
            abs_refer_path = os.path.abspath(ref_path).replace("\\", "/") if ref_path else ""
            params = {
                "text": text,
                "text_lang": "zh",
                "ref_audio_path": target_ref,
                # "aux_ref_audio_paths": aux_ref_audio_paths,
                "prompt_text": PROMPT_TEXT,
                "prompt_lang": PROMPT_LANG,
                "top_k": 5,
                "top_p": 0.95,
                "temperature": 0.9,
                "text_split_method": "cut5",
                "batch_size": 50,
                "seed": -1,
                "speed_factor": 1.1,
                "parallel_infer": True,
                "Repetition_Penalty": 1.4,
                "sample_steps": 128,
                "fragment_interval": 0.3
            }
            r = await http_client.post(SOVITS_API_URL, timeout=120.0, json=params, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                return base64.b64encode(r.content).decode("utf-8")
            logger.error("SOVITS API error %s - %s", r.status_code, r.text)
    except Exception as e:
        logger.exception(f"Voice synthesis exception: {e}")
    return None
# ================= 🚀 自动开机语音逻辑 =================
@driver.on_bot_connect
async def _(bot: Bot):
    """
    当机器人成功连接到服务器时，自动触发
    """
    # 1. 填入你想要接收开机语音的群号
    target_group = 712851492  # 替换成你的目标群号 
    
    # 2. 稍微延迟一下，等连接彻底稳定
    await asyncio.sleep(3) 
    
    logger.info(f"✨ 帕朵正在准备开机语音...")
    
    # 3. 设置帕朵的开机台词
    startup_text = "欸嘿嘿，祝大家新年快乐呀！帕朵在这里祝大家事业顺利！学业有成！哈哈"
    
    try:
        # 调用你插件里已有的语音合成函数
        # 注意：这里务必确保你的 get_sovits_audio 里的 batch_size 已经改成了 1
        
        audio_b64 = await get_sovits_audio(startup_text, REFER_WAV_PATH)
        if audio_b64:
            # 发送语音到指定群
            
            await bot.send_group_msg(
                group_id=target_group,
                message=MessageSegment.record(f"base64://{audio_b64}")
            )
            logger.info("✅ 帕朵开机语音发送成功！")
        else:
            logger.warning("❌ 帕朵开机语音合成失败了喵...")
            
    except Exception as e:
        logger.error(f"❌ 帕朵开机逻辑出现异常: {e}")

# =====================================================