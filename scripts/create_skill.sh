#!/bin/bash

##############################################################################
# Agent Skills - New Skill Scaffolding Script
#
# Usage:
#   ./scripts/create_skill.sh <skill-name>
#
# 功能说明:
# - 校验 skill 名称格式 (kebab-case)
# - 创建 skill 目录结构
# - 生成标准文档模板 (SKILL.md, README.md 等)
# - 更新 skills.json 注册新 skill
##############################################################################

set -e
set -u

# 引入工具库
source "$(dirname "$0")/utils.sh"

# 检查依赖
check_command jq

if [ $# -lt 1 ]; then
  log_error "Usage: $0 <skill-name>\nExample: $0 my-new-skill"
fi

SKILL_NAME=$1
SKILL_DIR="skills/$SKILL_NAME"
CONFIG_FILE="skills.json"

# 校验 skill 名称格式: 仅允许小写字母、数字和连字符，且不能以连字符开头或结尾
if [[ ! "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  log_error "Invalid skill name: '$SKILL_NAME'\nAllowed format: kebab-case (e.g., 'my-skill', 'data-processor')"
fi

if [ -d "$SKILL_DIR" ]; then
  log_error "Skill directory '$SKILL_DIR' already exists"
fi

log_step "Creating skill: $SKILL_NAME"

mkdir -p "$SKILL_DIR/assets/templates"
mkdir -p "$SKILL_DIR/references"
mkdir -p "$SKILL_DIR/scripts"

# 生成 SKILL.md
cat > "$SKILL_DIR/SKILL.md" <<EOF
---
name: $SKILL_NAME
description: |
  Description of what the $SKILL_NAME skill does.
  Define trigger phrases and usage scenarios here.
---

# $SKILL_NAME

Detailed documentation for the skill.

## Capabilities

1. Capability 1
2. Capability 2

## Usage

Example of how to use this skill.
EOF

# 生成 README.md
cat > "$SKILL_DIR/README.md" <<EOF
# $SKILL_NAME Skill

Description of the skill.

## Installation

\`\`\`bash
npx ${SKILL_NAME}-skill-installer
\`\`\`

## Usage

See SKILL.md for detailed instructions.
EOF

# 生成 INSTALL.md
cat > "$SKILL_DIR/INSTALL.md" <<EOF
# Installation Guide

## Automated Installation

\`\`\`bash
npx ${SKILL_NAME}-skill-installer
\`\`\`
EOF

log_step "Updating configuration..."

# 改进的作者信息获取逻辑：
# 1. 尝试从 skills.json 中获取任意一个现有 skill 的作者信息
# 2. 如果没有，使用 Git 配置
# 3. 最后回退到硬编码默认值
AUTHOR_NAME=$(jq -r '[.skills[].author.name][0] // empty' "$CONFIG_FILE")
if [ -z "$AUTHOR_NAME" ]; then
  AUTHOR_NAME=$(git config user.name 2>/dev/null || echo "Your Name")
fi

AUTHOR_EMAIL=$(jq -r '[.skills[].author.email][0] // empty' "$CONFIG_FILE")
if [ -z "$AUTHOR_EMAIL" ]; then
  AUTHOR_EMAIL=$(git config user.email 2>/dev/null || echo "your.email@example.com")
fi

tmp=$(mktemp)
if jq --arg name "$SKILL_NAME" \
   --arg author_name "$AUTHOR_NAME" \
   --arg author_email "$AUTHOR_EMAIL" \
   '.skills[$name] = {
     name: $name,
     displayName: ($name | ascii_upcase),
     version: "1.0.0",
     description: "Description for " + $name,
     author: {
       name: $author_name,
       email: $author_email
     },
     installer: {
       packageName: ($name + "-skill-installer"),
       binName: ("install-" + $name + "-skill")
     },
     files: {
       include: [
         "SKILL.md",
         "README.md",
         "INSTALL.md",
         "scripts",
         "references",
         "assets"
       ]
     },
     keywords: [$name, "agent-skill"]
   }' "$CONFIG_FILE" > "$tmp"; then
   mv "$tmp" "$CONFIG_FILE"
   log_success "Skill '$SKILL_NAME' created successfully!"
else
   rm "$tmp"
   log_error "Failed to update skills.json"
fi

echo ""
echo "Next steps:"
echo "1. Edit $SKILL_DIR/SKILL.md"
echo "2. Add your logic to $SKILL_DIR/scripts/"
echo "3. Run './scripts/publish.sh $SKILL_NAME 1.0.0' to publish"
echo ""
