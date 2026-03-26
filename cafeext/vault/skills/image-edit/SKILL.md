---
name: image-edit
description: "图像处理统筹技能。组合使用 mediainfo, imagemagick (magick/convert) 以及 spawn 多模态请求来完成「视觉识别 -> 元数据获取 -> 图像变换」的全生命周期管理。用于处理截图、照片修复、批量缩放或格式转换。"
---

# 图像统筹处理指南 (Image Process Orchestrator)

本技能不依赖单一脚本，而是通过统筹三个核心能力来实现对图像的“视觉级控制”。

## 1. 核心工具链

- **`spawn` (视觉识别)**: 使用多模态模型（如 `qwen3.5-35B-A3B`）来“看”图片内容，获取文本描述、元素坐标或缺陷位置。
- **`mediainfo` (元数据查询)**: 快速获取图片的 Dimens (长宽)、Color Space, DPI 和文件格式。
- **`imagemagick` (变换处理)**: 始终使用 `magick` (v7+) 命令执行裁剪、缩放、对比度增强或格式转换。

## 2. 标准工作流 (Orchestration Pattern)

### 第一步：视觉预判 (See)
在盲目处理前，先使用 `spawn` 分析图片。
> **示例**: "用 qwen3.5-35B-A3B 帮我看看这张图中二维码在哪个位置，有什么内容？"

### 第二步：参数核准 (Inspect)
使用 `mediainfo` 获取精准的物理参数，以决定处理阈值。
```bash
mediainfo --Output=JSON "<path_to_image>"
```

### 第三步：精确处理 (Process)
基于前两步的信息，使用 `magick` 进行精准变换。

**常用命令模板**:
- **高质量缩放**: `magick input.png -resize 1920x1080 output.png`
- **对比度/亮度自动增强**: `magick input.jpg -auto-level -auto-gamma output.jpg`
- **截图裁剪**: `magick input.png -crop <width>x<height>+<x>+<y> output.png`
- **OCR 预处理 (锐化+转灰度)**: `magick input.png -colorspace gray -sharpen 0x3 output_for_ocr.png`

## 3. 常见任务指南

### A. 移动端截图适配
1. 用 `mediainfo` 查看分辨率是否为高分屏 (Retina)。
2. 使用 `magick` 缩放 50% 以获得更小的文件体积。

### B. 多模态分析辅助
当模型“看不清”细节时：
1. 先用 `magick` 裁剪出模型描述的目标区域。
2. 再次调用 `spawn` 发起局部视觉分析请求。

## 4. 关键准则
- **原子化执行**: 不要尝试在一条命令中完成识别和处理，应分步执行并校验。
- **备份意识**: 在处理原始图片前，始终将处理结果输出到 `cafeext/workspace/downloads/` 或带 `_processed` 后缀。
- **工具手册**: 如遇复杂变换，先执行 `magick --help` 或 `magick convert --list operation` 查看支持的操作符。
