import os
from typing import Dict, Optional

# ================= 配置区域 =================
SOVITS_API_URL = "http://127.0.0.1:9880/tts"
REFER_WAV_PATH = "ref_audio/罐头.wav"  # 建议换成帕朵的参考音频
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
VOICE_KEYWORDS = ["语音", "声音", "唱歌", "听听", "想你了帕朵"]
TXT_KEYWORDS = ["帕朵"]