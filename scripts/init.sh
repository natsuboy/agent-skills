#!/bin/bash

##############################################################################
# Agent Skills - Repository Initialization Script
#
# Usage:
#   ./scripts/init.sh
#
# 功能说明:
# - 引导用户配置仓库信息（作者、仓库名等）
# - 更新 skills.json 配置文件
# - 更新文档中的占位符
##############################################################################

set -e
set -u

# 引入工具库
source "$(dirname "$0")/utils.sh"

# 检查依赖
check_command jq

CONFIG_FILE="skills.json"

if [ ! -f "$CONFIG_FILE" ]; then
  log_error "skills.json not found!"
fi

echo "=================================="
echo "🚀 Agent Skills - Init Repository"
echo "=================================="
echo ""

# 1. 收集信息
log_step "Configuration Setup"

# 尝试从 Git 配置获取默认值
# 使用 2>/dev/null 屏蔽错误输出
GIT_NAME=$(git config user.name 2>/dev/null || echo "Your Name")
GIT_EMAIL=$(git config user.email 2>/dev/null || echo "your.email@example.com")

# 读取当前配置作为默认值
# 使用 // "value" 处理可能的 null 值
CURRENT_OWNER=$(jq -r '.repository.owner // "YOUR_USERNAME"' "$CONFIG_FILE")
CURRENT_REPO=$(jq -r '.repository.repo // "agent-skills"' "$CONFIG_FILE")

# 尝试从现有 skill 中获取作者信息，如果没有则使用 Git 配置
CURRENT_AUTHOR_NAME=$(jq -r '[.skills[].author.name][0] // empty' "$CONFIG_FILE")
# 只有当变量为空时才使用默认值
CURRENT_AUTHOR_NAME=${CURRENT_AUTHOR_NAME:-$GIT_NAME}

CURRENT_AUTHOR_EMAIL=$(jq -r '[.skills[].author.email][0] // empty' "$CONFIG_FILE")
CURRENT_AUTHOR_EMAIL=${CURRENT_AUTHOR_EMAIL:-$GIT_EMAIL}

# 交互式提示
read -p "GitHub Username [$CURRENT_OWNER]: " INPUT_OWNER
OWNER=${INPUT_OWNER:-$CURRENT_OWNER}

read -p "Repository Name [$CURRENT_REPO]: " INPUT_REPO
REPO=${INPUT_REPO:-$CURRENT_REPO}

read -p "Author Name [$CURRENT_AUTHOR_NAME]: " INPUT_AUTHOR_NAME
AUTHOR_NAME=${INPUT_AUTHOR_NAME:-$CURRENT_AUTHOR_NAME}

read -p "Author Email [$CURRENT_AUTHOR_EMAIL]: " INPUT_AUTHOR_EMAIL
AUTHOR_EMAIL=${INPUT_AUTHOR_EMAIL:-$CURRENT_AUTHOR_EMAIL}

echo ""
echo "Summary:"
echo "  Owner: $OWNER"
echo "  Repo:  $REPO"
echo "  Name:  $AUTHOR_NAME"
echo "  Email: $AUTHOR_EMAIL"
echo ""

read -p "Proceed with updates? [Y/n] " CONFIRM
if [[ "$CONFIRM" =~ ^[Nn]$ ]]; then
  echo "Aborted."
  exit 0
fi

# 2. 更新 skills.json
log_step "Updating skills.json..."

tmp=$(mktemp)
# 使用 jq 更新顶层 repository 信息，并批量更新所有 skills 的作者信息
if jq --arg owner "$OWNER" \
   --arg repo "$REPO" \
   --arg name "$AUTHOR_NAME" \
   --arg email "$AUTHOR_EMAIL" \
   '.repository.owner = $owner | 
    .repository.repo = $repo | 
    .skills[] |= (.author.name = $name | .author.email = $email)' \
   "$CONFIG_FILE" > "$tmp"; then
   mv "$tmp" "$CONFIG_FILE"
   log_success "skills.json updated"
else
   rm "$tmp"
   log_error "Failed to update skills.json"
fi

# 3. 更新文档文件
log_step "Updating documentation placeholders..."

# 查找 markdown 文件并替换
# 排除 node_modules 和 .git
find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" | while read -r file; do
  UPDATED=false
  
  if grep -q "YOUR_USERNAME" "$file"; then
    SAFE_OWNER=$(escape_sed_pattern "$OWNER")
    portable_sed_inplace "s/YOUR_USERNAME/$SAFE_OWNER/g" "$file"
    UPDATED=true
  fi
  
  # 仅当 REPO 确实改变时才替换，且增加单词边界保护（如果可能），或简单字符串替换但需小心
  # 这里为了安全，我们只替换完全匹配 "agent-skills" 的字符串
  if [ "$REPO" != "agent-skills" ] && grep -q "agent-skills" "$file"; then
    SAFE_REPO=$(escape_sed_pattern "$REPO")
    portable_sed_inplace "s/agent-skills/$SAFE_REPO/g" "$file"
    UPDATED=true
  fi
  
  if [ "$UPDATED" = true ]; then
    echo "  Updated: $file"
  fi
done

log_success "Documentation updated"

# 4. 完成
echo ""
echo "=================================="
log_success "Initialization Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run './scripts/create_skill.sh <skill-name>' to add a new skill"
echo "2. Commit your changes: git commit -am 'Initialize repository'"
echo ""
