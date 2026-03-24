---
name: media-processor
description: "处理和编辑多媒体文件（图片、音频、视频）。使用 ffmpeg, imagemagick 和 mediainfo 工具执行转换、裁剪、提取元数据等操作。"
---

# 多媒体处理指南 (Media Processor)

当我需要处理图片、音频或视频文件时，我应该优先使用以下专业的命令行工具。

## 1. 核心工具推荐

- **ffmpeg**: 用于处理视频和音频（格式转换、剪辑、合并、提取音轨、压缩等）。
- **imagemagick** (命令通常为 `magick` 或 `convert`): 用于处理图片（尺寸调整、格式转换、滤镜、拼图等）。
- **mediainfo**: 用于快速查看多媒体文件的详细元数据（分辨率、编码、比特率、时长等）。

## 2. 遇到不懂的参数怎么办？

多媒体处理的命令行参数非常复杂且灵活。如果我对某个具体操作（例如“如何用 ffmpeg 提取视频前 10 秒并转为 gif”）不确定，我应该：

1. **主动上网搜索**: 使用 `web_search` 工具搜索关键词，例如 `ffmpeg extract segment to gif command`。
2. **查阅文档**: 参考搜索结果中的官方文档或 StackOverflow 上的最佳实践。
3. **小范围测试**: 先尝试一个简单的命令，确认无误后再进行大规模处理。

## 3. 相关项目与文档

- **FFmpeg**: https://ffmpeg.org/documentation.html
- **ImageMagick**: https://imagemagick.org/script/command-line-processing.php
- **MediaInfo**: https://mediaarea.net/en/MediaInfo

## 4. 我的执行准则

- 在执行任何可能耗时较长或占用大量磁盘空间的操作前，我会先告诉主人我的意图。
- 处理完成后，我会使用 `ls -lh` 检查生成的文件大小，并向主人汇报结果。
