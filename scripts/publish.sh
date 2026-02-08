#!/bin/bash

##############################################################################
# Agent Skills - 通用发布脚本
#
# 用法:
#   ./scripts/publish.sh <skill-name> <version>       # 发布单个 skill
#
# 示例:
#   ./scripts/publish.sh mermaid 1.0.0
#
# 此脚本会:
#   1. 从 skills.json 读取配置
#   2. 打包 skill 文件
#   3. 生成安装器（从模板）
#   4. 创建 release 文件和说明
##############################################################################

set -e
set -u

# 引入工具库
source "$(dirname "$0")/utils.sh"

# 检查依赖
check_dependencies() {
  local missing_deps=()
  
  if ! command -v jq &> /dev/null; then
    missing_deps+=("jq")
  fi
  
  if ! command -v node &> /dev/null; then
    missing_deps+=("node")
  fi
  
  if [ ${#missing_deps[@]} -gt 0 ]; then
    log_error "缺少必需依赖: ${missing_deps[*]}\n安装方法: brew install ${missing_deps[*]}"
  fi
}

# 读取 skill 配置
read_skill_config() {
  local skill_name=$1
  local config_file="skills.json"
  
  if [ ! -f "$config_file" ]; then
    log_error "配置文件不存在: $config_file"
  fi
  
  # 检查 skill 是否存在
  if ! jq -e ".skills.\"$skill_name\"" "$config_file" > /dev/null 2>&1; then
    log_error "Skill '$skill_name' 在 skills.json 中不存在"
  fi
  
  # 读取配置到全局变量
  SKILL_NAME=$skill_name
  SKILL_DISPLAY_NAME=$(jq -r ".skills.\"$skill_name\".displayName" "$config_file")
  SKILL_VERSION=$2
  SKILL_DESC=$(jq -r ".skills.\"$skill_name\".description" "$config_file")
  SKILL_DIR="skills/$skill_name"
  
  REPO_OWNER=$(jq -r ".repository.owner" "$config_file")
  REPO_NAME=$(jq -r ".repository.repo" "$config_file")
  
  INSTALLER_PKG=$(jq -r ".skills.\"$skill_name\".installer.packageName" "$config_file")
  INSTALLER_BIN=$(jq -r ".skills.\"$skill_name\".installer.binName" "$config_file")
  
  AUTHOR_NAME=$(jq -r ".skills.\"$skill_name\".author.name" "$config_file")
  AUTHOR_EMAIL=$(jq -r ".skills.\"$skill_name\".author.email" "$config_file")
  
  # 构建路径
  BUILD_DIR="build/$skill_name"
  INSTALLER_DIR="$BUILD_DIR/installer"
  PACKAGE_NAME="${skill_name}-skill.tar.gz"
  RELEASE_TAG="${skill_name}-v${SKILL_VERSION}"
  
  # 全局变量定义（确保 set -u 不报错）
  PACKAGE_SIZE=""
  SHA256=""
}

# 检查 skill 文件
check_skill_files() {
  log_step "1/7" "检查 skill 文件"
  
  if [ ! -d "$SKILL_DIR" ]; then
    log_error "Skill 目录不存在: $SKILL_DIR"
  fi
  
  if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    log_error "缺少核心文件: $SKILL_DIR/SKILL.md"
  fi
  
  log_success "文件检查通过"
  echo ""
}

# 清理并创建构建目录
prepare_build_dir() {
  log_step "2/7" "准备构建目录"
  
  rm -rf "$BUILD_DIR"
  mkdir -p "$BUILD_DIR"
  mkdir -p "$INSTALLER_DIR"
  
  log_success "构建目录已创建: $BUILD_DIR"
  echo ""
}

# 打包 skill
package_skill() {
  log_step "3/7" "打包 skill"
  
  # 准备暂存区
  local staging_dir="$BUILD_DIR/stage"
  local skill_staging_dir="$staging_dir/$SKILL_NAME"
  rm -rf "$staging_dir"
  mkdir -p "$skill_staging_dir"
  
  # 复制文件到暂存区 (修复空格文件遍历问题，避免子shell)
  while read -r file; do
    if [ -e "$SKILL_DIR/$file" ]; then
      cp -R "$SKILL_DIR/$file" "$skill_staging_dir/"
    else
      log_warning "文件不存在，跳过: $SKILL_DIR/$file"
    fi
  done < <(jq -r ".skills.\"$SKILL_NAME\".files.include[]" skills.json)
  
  # 清理排除的文件
  # 使用 -prune 避免 'No such file or directory' 警告
  find "$skill_staging_dir" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$skill_staging_dir" -name "*.pyc" -delete 2>/dev/null || true
  find "$skill_staging_dir" -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$skill_staging_dir" -name ".DS_Store" -delete 2>/dev/null || true
  find "$skill_staging_dir" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
  
  # 打包
  cd "$staging_dir"
  tar -czf "../$PACKAGE_NAME" "$SKILL_NAME"
  cd - > /dev/null
  
  # 清理暂存区
  rm -rf "$staging_dir"
  
  # 优化 du 输出处理 (使用 awk 提取第一列，更通用)
  PACKAGE_SIZE=$(du -h "$BUILD_DIR/$PACKAGE_NAME" | awk '{print $1}')
  log_success "Skill 包已创建: $PACKAGE_SIZE"
  echo ""
}

# 验证包内容
verify_package() {
  log_step "4/7" "验证包内容"
  
  local FILE_COUNT=$(tar -tzf "$BUILD_DIR/$PACKAGE_NAME" | wc -l | awk '{print $1}')
  log_success "包含 $FILE_COUNT 个文件"
  
  echo ""
  echo "目录结构预览:"
  tar -tzf "$BUILD_DIR/$PACKAGE_NAME" | head -20
  echo "..."
  echo ""
}

# 生成安装器
generate_installer() {
  log_step "5/7" "生成安装器"
  
  local TEMPLATE_FILE="$(dirname "$0")/templates/install.js.template"
  local OUTPUT_FILE="$INSTALLER_DIR/install.js"

  if [ ! -f "$TEMPLATE_FILE" ]; then
    log_error "模板文件未找到: $TEMPLATE_FILE"
  fi

  # 复制模板
  cp "$TEMPLATE_FILE" "$OUTPUT_FILE"

  # 替换占位符
  # 注意：在 Linux 和 macOS 上 sed 行为可能略有不同，utils.sh 提供了 portable_sed_inplace
  
  # 转义特殊字符，防止 sed 报错
  local SAFE_SKILL_NAME=$(escape_sed_pattern "$SKILL_NAME")
  local SAFE_SKILL_DISPLAY_NAME=$(escape_sed_pattern "$SKILL_DISPLAY_NAME")
  local SAFE_SKILL_VERSION=$(escape_sed_pattern "$SKILL_VERSION")
  local SAFE_REPO_OWNER=$(escape_sed_pattern "$REPO_OWNER")
  local SAFE_REPO_NAME=$(escape_sed_pattern "$REPO_NAME")
  local SAFE_RELEASE_TAG=$(escape_sed_pattern "$RELEASE_TAG")
  local SAFE_PACKAGE_NAME=$(escape_sed_pattern "$PACKAGE_NAME")
  local SAFE_INSTALLER_PKG=$(escape_sed_pattern "$INSTALLER_PKG")

  portable_sed_inplace "s/__SKILL_NAME__/$SAFE_SKILL_NAME/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__SKILL_DISPLAY_NAME__/$SAFE_SKILL_DISPLAY_NAME/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__SKILL_VERSION__/$SAFE_SKILL_VERSION/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__REPO_OWNER__/$SAFE_REPO_OWNER/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__REPO_NAME__/$SAFE_REPO_NAME/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__RELEASE_TAG__/$SAFE_RELEASE_TAG/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__PACKAGE_NAME__/$SAFE_PACKAGE_NAME/g" "$OUTPUT_FILE"
  portable_sed_inplace "s/__INSTALLER_PKG__/$SAFE_INSTALLER_PKG/g" "$OUTPUT_FILE"

  # 生成 package.json (使用 jq 构建 JSON 对象，更安全)
  # 安全读取 keywords，如果为空或不存在则返回 []
  local KEYWORDS_JSON=$(jq -c ".skills.\"$SKILL_NAME\".keywords // []" skills.json)
  
  # 使用 jq 构建完整的 package.json 内容
  jq -n \
    --arg name "$INSTALLER_PKG" \
    --arg version "$SKILL_VERSION" \
    --arg description "$SKILL_DESC" \
    --arg binName "$INSTALLER_BIN" \
    --argjson keywords "$KEYWORDS_JSON" \
    --arg authorName "$AUTHOR_NAME" \
    --arg authorEmail "$AUTHOR_EMAIL" \
    --arg repoUrl "https://github.com/$REPO_OWNER/$REPO_NAME.git" \
    --arg repoDir "skills/$SKILL_NAME" \
    --arg bugsUrl "https://github.com/$REPO_OWNER/$REPO_NAME/issues" \
    --arg homepage "https://github.com/$REPO_OWNER/$REPO_NAME/tree/main/skills/$SKILL_NAME" \
    '{
      name: $name,
      version: $version,
      description: $description,
      main: "install.js",
      bin: { ($binName): "install.js" },
      scripts: { test: "node install.js" },
      keywords: $keywords,
      author: { name: $authorName, email: $authorEmail },
      license: "MIT",
      repository: { type: "git", url: $repoUrl, directory: $repoDir },
      bugs: { url: $bugsUrl },
      homepage: $homepage
    }' > "$INSTALLER_DIR/package.json"

  chmod +x "$OUTPUT_FILE"
  
  log_success "安装器已生成"
  echo ""
}

# 生成校验和
generate_checksum() {
  log_step "6/7" "生成校验和"
  
  cd "$BUILD_DIR"
  
  # 获取跨平台 SHA256 命令
  local SHA256_CMD
  SHA256_CMD=$(get_sha256_cmd)
  $SHA256_CMD "$PACKAGE_NAME" > "$PACKAGE_NAME.sha256"
  
  SHA256=$(cat "$PACKAGE_NAME.sha256" | cut -d' ' -f1)
  cd - > /dev/null
  
  log_success "SHA256: $SHA256"
  echo ""
}

# 生成发布说明
generate_release_notes() {
  log_step "7/7" "生成发布说明"
  
  cat > "$BUILD_DIR/RELEASE_NOTES.md" <<EOF
# $SKILL_DISPLAY_NAME v$SKILL_VERSION

发布于 $(date '+%Y-%m-%d %H:%M:%S')

---

## 📦 下载

**Release Tag**: \`$RELEASE_TAG\`

- **Skill 包**: [\`$PACKAGE_NAME\`]($PACKAGE_NAME) ($PACKAGE_SIZE)
- **SHA256**: \`$SHA256\`

---

## 🚀 安装方法

### 方式1: 使用 npm 安装器（推荐）

\`\`\`bash
npx $INSTALLER_PKG
\`\`\`

### 方式2: 手动从 Release 下载

\`\`\`bash
# 下载
wget https://github.com/$REPO_OWNER/$REPO_NAME/releases/download/$RELEASE_TAG/$PACKAGE_NAME

# 解压到 skills 目录
tar -xzf $PACKAGE_NAME -C ~/.agents/skills/

# 验证安装
ls ~/.agents/skills/$SKILL_NAME/SKILL.md
\`\`\`

### 方式3: 从源码安装

\`\`\`bash
# 克隆仓库
git clone https://github.com/$REPO_OWNER/$REPO_NAME.git

# 复制到 skills 目录
cp -r $REPO_NAME/skills/$SKILL_NAME ~/.agents/skills/

# 验证安装
ls ~/.agents/skills/$SKILL_NAME/SKILL.md
\`\`\`

---

## ✨ 说明

$SKILL_DESC

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/$REPO_OWNER/$REPO_NAME
- **Skill 目录**: https://github.com/$REPO_OWNER/$REPO_NAME/tree/main/skills/$SKILL_NAME
- **问题反馈**: https://github.com/$REPO_OWNER/$REPO_NAME/issues

---

## 📝 更新日志

### v$SKILL_VERSION

- 初始发布

EOF
  
  log_success "发布说明已生成"
  echo ""
}

# 显示完成信息
show_completion() {
  echo "=================================="
  log_success "打包完成！"
  echo "=================================="
  echo ""
  
  echo "📦 发布文件:"
  echo "   $BUILD_DIR/$PACKAGE_NAME ($PACKAGE_SIZE)"
  echo "   $BUILD_DIR/$PACKAGE_NAME.sha256"
  echo "   $BUILD_DIR/RELEASE_NOTES.md"
  echo "   $INSTALLER_DIR/install.js"
  echo "   $INSTALLER_DIR/package.json"
  echo ""
  
  echo "📚 下一步:"
  echo ""
  echo "   1. 提交代码到 Git:"
  echo "      git add ."
  echo "      git commit -m \"$SKILL_NAME: v$SKILL_VERSION\""
  echo "      git tag $RELEASE_TAG"
  echo "      git push origin main --tags"
  echo ""
  echo "   2. 创建 GitHub Release:"
  echo "      - Tag: $RELEASE_TAG"
  echo "      - Title: $SKILL_DISPLAY_NAME v$SKILL_VERSION"
  echo "      - 上传: $BUILD_DIR/$PACKAGE_NAME"
  echo "      - 说明: 粘贴 $BUILD_DIR/RELEASE_NOTES.md"
  echo ""
  echo "   3. 发布 npm 安装器:"
  echo "      cd $INSTALLER_DIR"
  echo "      npm publish"
  echo ""
  echo "   4. 用户安装:"
  echo "      npx $INSTALLER_PKG"
  echo ""
}

# 主函数
main() {
  echo "=================================="
  echo "🚀 Agent Skills 发布工具"
  echo "=================================="
  echo ""
  
  # 检查参数
  if [ $# -lt 2 ]; then
    echo "用法: $0 <skill-name> <version>"
    echo ""
    echo "示例: $0 mermaid 1.0.0"
    exit 1
  fi
  
  # 检查依赖
  check_dependencies
  
  # 处理 --all
  if [ "$1" = "--all" ]; then
    log_error "--all 功能暂未实现，请逐个发布 skill"
  fi
  
  # 校验版本号格式
  if [[ ! "$2" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "版本号格式错误: '$2'\n应符合语义化版本规范: X.Y.Z (例如 1.0.0)"
  fi
  
  # 读取配置
  read_skill_config "$1" "$2"
  
  echo "Skill: $SKILL_DISPLAY_NAME"
  echo "版本: v$SKILL_VERSION"
  echo "标签: $RELEASE_TAG"
  echo ""
  
  # 执行打包流程
  check_skill_files
  prepare_build_dir
  package_skill
  verify_package
  generate_installer
  generate_checksum
  generate_release_notes
  
  # 显示完成信息
  show_completion
}

# 运行
main "$@"
