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

# 获取 SHA256 命令
get_sha256_cmd() {
  if command -v shasum &> /dev/null; then
    echo "shasum -a 256"
  elif command -v sha256sum &> /dev/null; then
    echo "sha256sum"
  else
    log_error "Neither shasum nor sha256sum found. Please install coreutils (Linux) or check your path."
  fi
}

# 检查命令是否存在
check_command() {
  if ! command -v "$1" &> /dev/null; then
    log_error "Missing dependency: $1\nInstall it via: brew install $1 (macOS) or apt-get install $1 (Linux)"
  fi
}
