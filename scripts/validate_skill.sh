#!/bin/bash

##############################################################################
# Agent Skills - Skill 验证脚本
#
# 用法:
#   ./scripts/validate_skill.sh [skill-name]
#
# 示例:
#   ./scripts/validate_skill.sh mermaid      # 验证单个 skill
#   ./scripts/validate_skill.sh              # 验证所有 skills
#
# 验证内容:
#   1. SKILL.md 存在性
#   2. YAML frontmatter 格式
#   3. 必需字段（name, description）
#   4. README.md 存在性
#   5. skills.json 配置一致性
##############################################################################

set -e
set -u

# 引入工具库
source "$(dirname "$0")/utils.sh"

# 全局变量
VALIDATION_FAILED=0
SKILL_COUNT=0
SUCCESS_COUNT=0

# 验证单个 skill
validate_single_skill() {
  local skill_name=$1
  local skill_dir="skills/$skill_name"
  local skill_file="$skill_dir/SKILL.md"

  SKILL_COUNT=$((SKILL_COUNT + 1))

  echo ""
  log_step "验证 skill: $skill_name"

  # 1. 检查目录存在
  if [ ! -d "$skill_dir" ]; then
    log_error "Skill 目录不存在: $skill_dir"
    return
  fi

  # 2. 检查 SKILL.md 存在
  if [ ! -f "$skill_file" ]; then
    log_error "缺少核心文件: $skill_file"
    VALIDATION_FAILED=1
    return
  fi
  log_success "SKILL.md 存在"

  # 3. 验证 YAML frontmatter
  validate_yaml_frontmatter "$skill_file" 2>/dev/null || {
    VALIDATION_FAILED=1
    return
  }
  log_success "YAML frontmatter 格式正确"

  # 4. 提取并显示必需字段
  local name=$(extract_yaml_field "$skill_dir" "name")
  local description=$(extract_yaml_field "$skill_dir" "description")

  if [ -n "$name" ]; then
    echo "   → name: $name"
  fi

  if [ -n "$description" ]; then
    echo "   → description: ${description:0:60}..."
  fi

  # 5. 检查 README.md
  if [ ! -f "$skill_dir/README.md" ]; then
    log_warning "缺少 README.md（推荐添加）"
  else
    log_success "README.md 存在"
  fi

  # 6. 验证 skills.json 配置
  if ! jq -e ".skills.\"$skill_name\"" skills.json > /dev/null 2>&1; then
    log_warning "skill 未在 skills.json 中注册"
  else
    local json_name=$(get_skill_config "$skill_name" "name")
    local json_display_name=$(get_skill_config "$skill_name" "displayName")

    # 检查名称一致性
    if [ "$json_name" != "$skill_name" ]; then
      log_error "skills.json 中 name 不匹配: $json_name vs $skill_name"
      VALIDATION_FAILED=1
    else
      log_success "skills.json 配置正确"
      echo "   → displayName: $json_display_name"
    fi
  fi

  # 7. 检查目录结构（可选）
  local subdirs=$(find "$skill_dir" -maxdepth 1 -type d -not -path "$skill_dir" -not -path "*/.*" | wc -l | tr -d ' ')
  if [ "$subdirs" -gt 0 ]; then
    echo "   → 子目录: $(find "$skill_dir" -maxdepth 1 -type d -not -path "$skill_dir" -not -path "*/.*" -exec basename {} \; | tr '\n' ' ')"
  fi

  SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
}

# 验证所有 skills
validate_all_skills() {
  echo "=================================="
  log_step "验证所有 skills"
  echo "=================================="

  # 获取所有 skill 名称
  local all_skills=$(get_all_skills)

  if [ -z "$all_skills" ]; then
    log_error "未在 skills.json 中找到任何 skills"
  fi

  # 逐个验证
  while IFS= read -r skill_name; do
    validate_single_skill "$skill_name"
  done <<< "$all_skills"

  # 显示汇总
  echo ""
  echo "=================================="
  log_step "验证汇总"
  echo "=================================="
  echo "总计: $SKILL_COUNT 个 skills"
  echo "成功: $SUCCESS_COUNT 个"

  if [ "$VALIDATION_FAILED" -eq 1 ]; then
    log_error "验证失败，请检查上述错误"
  else
    log_success "所有 skills 验证通过！"
  fi
  echo "=================================="
}

# 主函数
main() {
  echo "=================================="
  echo "🔍 Agent Skills 验证工具"
  echo "=================================="

  # 检查参数
  if [ $# -eq 0 ]; then
    # 无参数：验证所有 skills
    validate_all_skills
  elif [ $# -eq 1 ]; then
    # 有参数：验证单个 skill
    local skill_name=$1

    if ! skill_exists "$skill_name"; then
      log_error "Skill 不存在: $skill_name"
    fi

    validate_single_skill "$skill_name"

    echo ""
    if [ "$VALIDATION_FAILED" -eq 1 ]; then
      log_error "验证失败，请检查上述错误"
    else
      log_success "Skill '$skill_name' 验证通过！"
    fi
  else
    echo "用法: $0 [skill-name]"
    echo ""
    echo "示例:"
    echo "  $0 mermaid      # 验证单个 skill"
    echo "  $0              # 验证所有 skills"
    exit 1
  fi
}

# 运行
main "$@"
