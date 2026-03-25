"Google Imagen 生图集成工具。
支持文本提示词与多参考图融合。
"

import os
import time
import base64
from pathlib import Path
from typing import Any, List, Optional
import google.generativeai as genai
from loguru import logger

from nanobot.agent.tools.base import Tool
from cafeext.py.wrapper.config import WORKSPACE_DIR

class GoogleImageGenTool(Tool):
    """使用 Google Imagen 模型生成图像的工具。"""

    def __init__(self):
        super().__init__()
        # 从环境变量或 .env 读取 Key
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            logger.warning("GOOGLE_API_KEY not found in environment.")

    @property
    def name(self) -> str:
        return "google-image-gen"

    @property
    def description(self) -> str:
        return "使用 Google Imagen 模型（Nano Banana）根据文本描述生成图像。支持传入一个或多个本地图片路径作为创作参考。"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "图像的详细文本描述（Prompt）。"
                },
                "reference_images": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可选：用作参考的本地图片物理路径列表。"
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["1:1", "3:2", "4:3", "9:16", "16:9"],
                    "default": "1:1",
                    "description": "生成图像的纵横比。"
                }
            },
            "required": ["prompt"]
        }

    async def execute(self, prompt: str, reference_images: Optional[List[str]] = None, aspect_ratio: str = "1:1") -> str:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY is not configured."

        try:
            # 1. 准备模型 (Nano Banana 2)
            model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
            
            # 2. 准备内容负载
            contents = [prompt]
            
            if reference_images:
                for img_path in reference_images:
                    p = Path(img_path)
                    if p.exists() and p.is_file():
                        # 读取并包装为 SDK 要求的格式
                        img_data = p.read_bytes()
                        # 简单推断 mime 类型
                        mime_type = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
                        contents.append({
                            "mime_type": mime_type,
                            "data": img_data
                        })
                    else:
                        logger.warning(f"Reference image not found: {img_path}")

            # 3. 调用生成
            # 注意：实际 API 参数可能随 SDK 版本微调，这里使用标准 generate_content 模式
            # 若 Imagen 3 有专属 API 接口，需按最新文档适配
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            response = model.generate_content(contents)
            
            # 4. 处理响应
            if not response.candidates:
                return "Error: No image candidates returned from Google API."
            
            # 假设生成的图像在第一个 candidate 的第一个 part
            # 结构参考：candidates[0].content.parts[0].inline_data.data
            try:
                # 某些版本中，图片直接作为 inline_data 返回
                part = response.candidates[0].content.parts[0]
                if hasattr(part, "inline_data"):
                    img_bytes = part.inline_data.data
                elif hasattr(part, "data"):
                    img_bytes = part.data
                else:
                    return f"Error: Unexpected response format from API. Part keys: {dir(part)}"
            except Exception as e:
                return f"Error: Failed to extract image data from response: {e}"

            # 5. 保存图片
            output_dir = WORKSPACE_DIR / "media" / "generated"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"gen-{timestamp}.png"
            output_path = output_dir / filename
            
            with open(output_path, "wb") as f:
                f.write(img_bytes)

            logger.info(f"Image generated and saved to: {output_path}")
            
            return f"🎨 图像生成成功！\n- 保存路径: `{output_path}`\n- 提示词: {prompt}\n\n我已经将生成的图片保存到了你的媒体库中，你可以随时查看。"

        except Exception as e:
            error_msg = f"❌ 图像生成失败。\n- 错误原因: {str(e)}\n- 建议: 请检查 API Key 是否有效，或稍后重试。"
            logger.error(f"Image generation failed: {e}")
            return error_msg

def apply_image_gen_patch():
    """动态注册生图工具。"""
    try:
        from nanobot.agent.loop import AgentLoop
        
        original_register = AgentLoop._register_default_tools
        
        def patched_register(self):
            # 先跑原有的注册逻辑
            original_register(self)
            # 再塞进咱们的新工具
            self.tools.register(GoogleImageGenTool())
            logger.info("Custom tool 'google-image-gen' registered.")

        AgentLoop._register_default_tools = patched_register
        
    except Exception as e:
        logger.error(f"Failed to apply image gen patch: {e}")
