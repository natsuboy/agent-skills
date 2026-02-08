#!/bin/bash

##############################################################################
# Agent Skills - 通用工具库
#
# 功能说明:
# - 定义颜色常量
# - 提供日志输出函数
# - 提供跨平台兼容性函数 (sed)
# - 提供依赖检查函数
##############################################################################

# 严格模式
set -u

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 日志函数 (输出到 stderr 以避免污染 stdout)
log_step() { 
  if [ $# -eq 1 ]; then
    echo -e "${CYAN}[Step]${NC} $1" >&2
  else
    echo -e "${CYAN}[$1]${NC} $2" >&2
  fi
}
log_success() { echo -e "${GREEN}✅${NC} $1" >&2; }
log_error() { echo -e "${RED}❌${NC} $1" >&2; exit 1; }
log_warning() { echo -e "${YELLOW}⚠️${NC} $1" >&2; }

# 跨平台 sed -i 替换函数
portable_sed_inplace() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS (BSD sed)
    sed -i '' "$@"
  else
    # Linux (GNU sed)
    sed -i "$@"
  fi
}

# 转义 sed 替换字符串中的特殊字符
escape_sed_pattern() {
  echo "$1" | sed 's/[&/\]/\\&/g'
}

# 检查命令是否存在
check_command() {
  if ! command -v "$1" &> /dev/null; then
    log_error "Missing dependency: $1\nInstall it via: brew install $1 (macOS) or apt-get install $1 (Linux)"
  fi
}

# 验证版本号格式（语义化版本）
validate_version() {
  local version="$1"
  if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "版本号格式错误: '$version'\n应符合语义化版本规范: X.Y.Z (例如 1.0.0)"
  fi
}

# 提取 SKILL.md 的 YAML frontmatter 字段
extract_yaml_field() {
  local skill_dir="$1"
  local field="$2"
  local skill_file="$skill_dir/SKILL.md"

  if [ ! -f "$skill_file" ]; then
    echo ""
    return
  fi

  # 提取 YAML frontmatter 中的字段
  awk 'BEGIN {p=0}
  /^---$/ {if (p) exit; else {p=1; next}}
  p && /'"$field"':/ {
    sub(/'"$field"':[[:space:]]*/, "")
    if (!/^[|>]/) {
      print
      exit
    }
    next
  }
  p && /^[[:space:]]/ && !/^[[:space:]]*[|>]/ {
    print
  }' "$skill_file" | head -20 | sed 's/^[[:space:]]*//' | tr '\n' ' ' | xargs
}

# 获取 skills.json 中的 skill 配置
get_skill_config() {
  local skill_name="$1"
  local field="$2"

  jq -r ".skills.\"$skill_name\".$field // \"\"" skills.json 2>/dev/null
}

# 获取所有 skill 名称列表
get_all_skills() {
  jq -r '.skills | keys[]' skills.json 2>/dev/null
}

# 检查 skill 是否存在
skill_exists() {
  local skill_name="$1"
  [ -d "skills/$skill_name" ] && [ -f "skills/$skill_name/SKILL.md" ]
}

# 验证 YAML frontmatter 格式
validate_yaml_frontmatter() {
  local skill_file="$1"

  # 检查是否有 --- 包围的 frontmatter
  if ! grep -q "^---$" "$skill_file"; then
    log_error "SKILL.md 缺少 YAML frontmatter（必须用 --- 包围）"
  fi

  # 检查必需字段
  local name=$(extract_yaml_field "$(dirname "$skill_file")" "name")
  local description=$(extract_yaml_field "$(dirname "$skill_file")" "description")

  if [ -z "$name" ]; then
    log_error "SKILL.md 缺少必需字段: name"
  fi

  if [ -z "$description" ]; then
    log_error "SKILL.md 缺少必需字段: description"
  fi
}
