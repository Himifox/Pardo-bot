import asyncio
import pyvts
# 初始化 VTS 客户端信息
plugin_info = {
    "plugin_name": "AI_VTuber_Controller",
    "developer": "YourName",
    # 认证 token 会保存在本地，之后就不用每次都在 VTS 里点允许了
    "authentication_token_path": "./vts_token.txt" 
}

vts = pyvts.vts(plugin_info=plugin_info)

async def main():
    # 1. 连接到 VTube Studio
    print("正在连接到 VTube Studio...")
    await vts.connect()
    print("连接成功！")

    # 2. 身份验证
    # 注意：第一次运行这个脚本时，VTube Studio 画面中会弹出一个窗口，你需要手动点击“允许(Allow)”
    print("正在进行身份验证...")
    await vts.request_authenticate_token()
    await vts.request_authenticate()
    print("身份验证完成！")

    # 3. 获取当前 Live2D 模型的所有可用热键 (Hotkeys/表情动作)
    try:
        response = await vts.request("HotkeysInCurrentModel", modelID=None)
        print("接口返回数据：", response['data'])
        hotkeys = response['data'].get('availableHotkeys') or response['data'].get('hotkeys') or []
    except Exception as e:
        print("获取热键时发生异常：", e)
        hotkeys = []
    
    print("\n--- 当前模型可用的热键有 ---")
    for hk in hotkeys:
        print(f"名称: {hk['name']}, ID: {hk['hotkeyID']}")
    print("----------------------------\n")

    # 4. 模拟大语言模型生成的带有“情感标签”的回复
    # 比如识别到特定的词或表情符，让模型做出对应的动作
    llm_response = "[smile] 老板，这单生意可不亏哦！"
    print(f"收到 LLM 回复: {llm_response}")

    # 5. 解析标签并触发对应表情
    if "[smile]" in llm_response:
        print("检测到 [smile] 标签，正在匹配模型表情...")
        
        # 遍历热键列表，寻找名称包含 "smile" 或你自定义名称的热键
        # (请确保你的 VTS 模型里提前设置好了名为 "smile" 的表情快捷键)
        for hk in hotkeys:
            if "smile" in hk['name'].lower() or "笑" in hk['name']:
                # 发送触发表情的请求
                await vts.request("TriggerHotkey", hotkeyID=hk['hotkeyID'])
                print(f"-> 已成功触发表情: {hk['name']}")
                break
    
    # 保持连接运行几秒钟，让你能在 VTS 里看到表情变化
    await asyncio.sleep(5)
    
    # 养成良好习惯，用完关闭连接
    await vts.close()

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())