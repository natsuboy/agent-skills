#!/bin/bash

##############################################################################
# Agent Skills - Skill 预览脚本
#
# 用法:
#   ./scripts/preview_skill.sh [skill-name]
#
# 示例:
#   ./scripts/preview_skill.sh mermaid      # 预览单个 skill
#   ./scripts/preview_skill.sh              # 列出所有 skills
#
# 功能:
#   1. 显示 skill 的基本信息（name, description）
#   2. 显示安装命令
#   3. 列出 skill 的文件结构
#   4. 模拟 skills.sh CLI 的扫描行为
##############################################################################

set -e
set -u

# 引入工具库
source "$(dirname "$0")/utils.sh"

# 绘制边框的函数
draw_box() {
  local title=$1
  local width=${2:-70}

  echo ""
  printf "┌─"
  printf "%0.s─" $(seq 1 $((width - ${#title} - 4)))
  printf " %s " "$title"
  printf "%0.s─" $(seq 1 $((width - ${#title} - 4)))
  printf "─┐\n"
}

draw_separator() {
  local width=${1:-70}
  printf "│"
  printf "%0.s " $(seq 1 $((width - 2)))
  printf "│\n"
}

draw_line() {
  local text=$1
  local width=${2:-70}

  printf "│ %s" "$text"
  local text_len=${#text}
  printf "%0.s " $(seq 1 $((width - text_len - 4)))
  printf "│\n"
}

draw_footer() {
  local width=${1:-70}
  printf "│"
  printf "%0.s─" $(seq 1 $((width - 2)))
  printf "│\n"
}

draw_end() {
  local width=${1:-70}
  printf "└"
  printf "%0.s─" $(seq 1 $((width - 2)))
  printf "┘\n"
}

# 预览单个 skill
preview_single_skill() {
  local skill_name=$1
  local skill_dir="skills/$skill_name"
  local width=80

  draw_box "$skill_name" "$width"

  # 基本信息
  local name=$(extract_yaml_field "$skill_dir" "name")
  local description=$(extract_yaml_field "$skill_dir" "description")
  local display_name=$(get_skill_config "$skill_name" "displayName")
  local version=$(get_skill_config "$skill_name" "version")
  local repo_owner=$(jq -r ".repository.owner" skills.json)
  local repo_name=$(jq -r ".repository.repo" skills.json)

  draw_separator "$width"
  draw_line "名称: $display_name" "$width"
  draw_line "标识: $name" "$width"
  draw_line "版本: v$version" "$width"

  draw_separator "$width"
  draw_line "描述:" "$width"
  draw_separator "$width"

  # 分行显示描述（每行最多 60 字符）
  if [ -n "$description" ]; then
    echo "$description" | fold -s -w 60 | while read -r line; do
      draw_line "  $line" "$width"
    done
  fi

  draw_separator "$width"

  # 安装命令
  draw_line "安装命令:" "$width"
  draw_separator "$width"
  draw_line "  npx skills add ${repo_owner}/${repo_name} --skill $skill_name" "$width"

  draw_separator "$width"

  # 文件结构
  local file_count=$(find "$skill_dir" -type f 2>/dev/null | wc -l | tr -d ' ')
  local dir_count=$(find "$skill_dir" -type d 2>/dev/null | wc -l | tr -d ' ')

  draw_line "文件结构 ($file_count 个文件, $dir_count 个目录):" "$width"
  draw_separator "$width"

  # 显示前 20 个文件/目录
  find "$skill_dir" -maxdepth 3 -not -path "$skill_dir" -not -path "*/.*" | sort | head -20 | while read -r item; do
    local item_name=$(basename "$item")
    local indent="  "
    if [ -d "$item" ]; then
      draw_line "${indent}📁 $item_name/" "$width"
    else
      draw_line "${indent}📄 $item_name" "$width"
    fi
  done

  if [ $((file_count + dir_count)) -gt 20 ]; then
    draw_line "  ... (还有 $((file_count + dir_count - 20)) 个文件)" "$width"
  fi

  draw_separator "$width"

  # YAML frontmatter 预览
  draw_line "SKILL.md frontmatter:" "$width"
  draw_separator "$width"
  awk '/^---$/,/^---$/{if (!/^---$/) print "  " $0}' "$skill_dir/SKILL.md" | head -10

  draw_footer "$width"
  draw_end "$width"
}

# 列出所有 skills
list_all_skills() {
  echo ""
  echo "=================================="
  log_step "所有可用 Skills"
  echo "=================================="
  echo ""

  local all_skills=$(get_all_skills)
  local index=1
  local repo_owner=$(jq -r ".repository.owner" skills.json)
  local repo_name=$(jq -r ".repository.repo" skills.json)

  echo "安装所有 skills:"
  echo "  npx skills add ${repo_owner}/${repo_name}"
  echo ""
  echo "----------------------------------"
  echo ""

  # 逐个列出
  while IFS= read -r skill_name; do
    local display_name=$(get_skill_config "$skill_name" "displayName")
    local description=$(get_skill_config "$skill_name" "description")
    local version=$(get_skill_config "$skill_name" "version")

    printf "%2d. [%s] %s\n" "$index" "$skill_name" "$display_name"
    printf "    版本: v%s\n" "$version"
    printf "    描述: %s\n" "${description:0:60}..."
    printf "    安装: npx skills add %s/%s --skill %s\n\n" "$repo_owner" "$repo_name" "$skill_name"

    index=$((index + 1))
  done <<< "$all_skills"

  echo "----------------------------------"
  echo "总计: $((index - 1)) 个 skills"
  echo "=================================="
  echo ""
}

# 主函数
main() {
  echo "=================================="
  echo "👀 Agent Skills 预览工具"
  echo "=================================="

  # 检查参数
  if [ $# -eq 0 ]; then
    # 无参数：列出所有 skills
    list_all_skills
  elif [ $# -eq 1 ]; then
    # 有参数：预览单个 skill
    local skill_name=$1

    if ! skill_exists "$skill_name"; then
      log_error "Skill 不存在: $skill_name\n可用 skills: $(get_all_skills | tr '\n' ' ')"
    fi

    preview_single_skill "$skill_name"
  else
    echo "用法: $0 [skill-name]"
    echo ""
    echo "示例:"
    echo "  $0 mermaid      # 预览单个 skill"
    echo "  $0              # 列出所有 skills"
    exit 1
  fi
}

# 运行
main "$@"
