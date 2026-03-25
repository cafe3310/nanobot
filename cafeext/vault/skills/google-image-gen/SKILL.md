---
name: google-image-gen
description: "使用 Google Nano Banana (Imagen) 模型生成或编辑图像。"
---

# 图像生成指南 (Google Imagen)

你可以通过此工具调用 Google 的 Imagen 模型（社区代称 Nano Banana）来创作视觉内容。

## 核心功能

1. **文生图**: 根据你提供的详细描述（Prompt）从无到有生成图片。
2. **图文生图 (Image-to-Image)**: 传入一张或多张本地图片作为参考，结合文字描述进行创作。
3. **风格迁移与融合**: 通过多图参考，实现不同主题或风格的融合。

## 使用建议

- **描述词要具体**: 包含主体、背景、构图、光影和画风（如：`photorealistic`, `3D render`, `oil painting`）。
- **善用参考图**: 如果想保持角色一致性，请务必传入包含该角色的参考图路径。
- **纵横比选择**: 默认 1:1，但你可以根据需要选择 `16:9`（海报/壁纸）或 `9:16`（手机尺寸）。

## 示例

```python
# 示例 1: 简单的文生图
google-image-gen(prompt="一只穿着红色斗篷在雨中奔跑的柯基，赛博朋克画风")

# 示例 2: 带参考图的创作
google-image-gen(
    prompt="让照片里的这只猫飞向太空", 
    reference_images=["/path/to/my_cat.png"],
    aspect_ratio="16:9"
)
```

## 注意事项

- 生成过程通常需要 10-20 秒，请耐心等待。
- 所有生成的图片都会保存至 `cafeext/workspace/media/generated/`。
- 如果 API 报错，请先确认 `cafeext/.env` 中的 `GOOGLE_API_KEY` 是否配置正确。
