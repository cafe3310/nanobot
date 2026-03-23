"""Sidecar 核心配置中心。
集中管理路径、安全策略、日志表现等所有定制化参数。
"""

from pathlib import Path

# --- 1. 基础路径配置 (Base Paths) ---
WRAPER_DIR = Path(__file__).parent.absolute()
CAFEEXT_DIR = WRAPER_DIR.parent.parent.absolute()
PROJECT_ROOT = CAFEEXT_DIR.parent.absolute()

# 核心数据目录
WORKSPACE_DIR = CAFEEXT_DIR / "workspace"
VAULT_DIR = CAFEEXT_DIR / "vault"
LOG_DIR = CAFEEXT_DIR / "logs"

# 配置文件与密钥
CONFIG_JSON_PATH = CAFEEXT_DIR / "config.json"
DOTENV_PATH = CAFEEXT_DIR / ".env"

# --- 2. 安全策略配置 (Security Policy) ---

# 强制禁用的 Agent Skills (文件夹名)
DISABLED_SKILLS = ["clawhub"]

# 强制禁用的核心工具 (Tool Name)
DISABLED_TOOLS = []

# --- 3. 优雅日志表现 (Elegant Logging) ---

# 日志文件后缀 (使用 .log 强调人类可读性)
LOG_SUFFIX = ".log"

# 分隔符
LOG_SEPARATOR = "=" * 30

# 事件类型与 Emoji 映射
EMOJI_MAP = {
    "request": "🚀 推理请求",
    "success": "✨ 推理成功",
    "failure": "❌ 推理失败",
    "tool_start": "🛠️ 工具执行",
    "tool_end": "📦 工具响应",
    "tool_error": "⚠️ 工具报错",
    "inbound": "📥 收到消息",
    "outbound": "📤 发送回复"
}

# --- 4. 记忆金库逻辑 (Vault Schema) ---

# 三位一体记忆文件名
VAULT_FILES = {
    "soul": "SOUL.md",   # 核心灵魂 (只读)
    "user": "USER.md",   # 主人设定 (只读)
    "bot": "BOT.md"      # 对话经验 (内部读写)
}
