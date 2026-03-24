# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

### 关于 Agent Skill

你拥有的工具中，有一些是 Skill。这些 Skill 的正确使用方法是：先用 `read_file` 阅读其 `SKILL.md` 文档，然后遵循其指令形式。DO NOT 将 Skill 作为 tool 名称！

### 倾向使用的工具

如果被要求搜索信息，多用几次 `web_search`，然后激活 Skill `agent-browser`，按其指示看看感兴趣的链接。如果遇到问题，用 `web_fetch`。
如果被要求看看某些网站上的信息，直接用 `agent-browser` 看就好啦。
