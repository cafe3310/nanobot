"""macOS 原生通知交互模块。"""

import subprocess
import json

def ask_macos_permission(name, params):
    """
    通过 AppleScript 弹出 macOS 原生对话框。
    返回: True (允许), False (拒绝), None (系统错误/无法弹出)
    """
    try:
        # 1. 参数美化
        try:
            params_json = json.dumps(params, ensure_ascii=False, indent=1)
            if len(params_json) > 400:
                params_json = params_json[:400] + "..."
        except:
            params_json = str(params)
        
        # 2. 构造文本（针对 AppleScript 进行严格转义）
        text = f"是否允许 nanobot 执行工具：{name}？\n\n参数预览：\n{params_json}"
        
        # 核心转义逻辑：
        # a. 将双引号转义为 \"
        # b. 将换行符转义为 \n 字符串
        safe_text = text.replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
        title = "nanobot 🐈 安全确认"

        # 3. 核心脚本：
        # 使用 -e 指令执行单行脚本，减少多行带来的解析风险
        script = (
            f'tell application (path to frontmost application as text) to ' 
            f'display dialog "{safe_text}" ' 
            f'with title "{title}" ' 
            f'buttons {{"Deny", "Allow"}} ' 
            f'default button "Deny" ' 
            f'with icon note'
        )
        
        # 4. 执行
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            # 可能是权限问题或用户取消
            return None
            
        # AppleScript 返回格式通常为 "button returned:Allow"
        if "Allow" in result.stdout:
            return True
        if "Deny" in result.stdout:
            return False
            
        return None
        
    except Exception:
        return None
