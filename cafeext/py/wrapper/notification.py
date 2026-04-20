"""
=== cafe3310 nanobot sidecar function ===
注入点：由 security.py 调用。
作用：封装 macOS 原生通知交互。通过 AppleScript 弹出带按钮的对话框，为高风险工具操作提供 Human-in-the-loop 的本地物理确认。
=== end(keep this block) ===
"""

import subprocess
import json

def ask_macos_permission(name, params):
    """
    通过 AppleScript 弹出 macOS 原生对话框。
    采用位置参数传递文本，彻底解决转义字符导致的弹窗失败问题。
    """
    try:
        # 1. 准备参数预览
        try:
            params_json = json.dumps(params, ensure_ascii=False, indent=1)
            # 限制长度，防止对话框撑爆屏幕
            if len(params_json) > 1000:
                params_json = params_json[:1000] + "\n... (truncated)"
        except:
            params_json = str(params)
        
        # 2. 构造文本内容
        display_text = f"是否允许 nanobot 执行工具：{name}？\n\n参数预览：\n{params_json}"
        title = "nanobot 🐈 安全确认"

        # 3. 编写 AppleScript
        # 使用 'on run argv' 接收外部参数，避免在 script 字符串中进行复杂的插值和转义
        script = '''
        on run argv
            set display_text to item 1 of argv
            set dialog_title to item 2 of argv
            
            tell application (path to frontmost application as text)
                try
                    set res to display dialog display_text with title dialog_title buttons {"Deny", "Allow"} default button "Deny" with icon note
                    return button returned of res
                on error
                    return "Error"
                end try
            end tell
        end run
        '''
        
        # 4. 执行 osascript 并通过 argv 传递文本
        result = subprocess.run(
            ["osascript", "-e", script, display_text, title],
            capture_output=True,
            text=True,
            timeout=120 # 调大超时时间，给用户充足的思考时间
        )
        
        if result.returncode != 0:
            # 执行失败（通常是权限问题）
            return None
            
        stdout = result.stdout.strip()
        if "Allow" in stdout:
            return True
        if "Deny" in stdout:
            return False
            
        return None
        
    except subprocess.TimeoutExpired:
        print("🕒 macOS Dialog timed out.")
        return None
    except Exception as e:
        # print(f"DEBUG: Notification error: {e}")
        return None
