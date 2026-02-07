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

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 工具函数
log_step() {
  echo -e "${CYAN}[$1]${NC} $2"
}

log_success() {
  echo -e "${GREEN}✅${NC} $1"
}

log_error() {
  echo -e "${RED}❌${NC} $1"
  exit 1
}

log_warning() {
  echo -e "${YELLOW}⚠️${NC} $1"
}

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
  INSTALLER_SCOPE=$(jq -r ".skills.\"$skill_name\".installer.scope" "$config_file")
  INSTALLER_BIN=$(jq -r ".skills.\"$skill_name\".installer.binName" "$config_file")
  
  AUTHOR_NAME=$(jq -r ".skills.\"$skill_name\".author.name" "$config_file")
  AUTHOR_EMAIL=$(jq -r ".skills.\"$skill_name\".author.email" "$config_file")
  
  # 构建路径
  BUILD_DIR="build/$skill_name"
  INSTALLER_DIR="$BUILD_DIR/installer"
  PACKAGE_NAME="${skill_name}-skill.tar.gz"
  RELEASE_TAG="${skill_name}-v${SKILL_VERSION}"
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
  
  # 读取要包含的文件
  local include_files=$(jq -r ".skills.\"$SKILL_NAME\".files.include[]" skills.json)
  
  # 复制文件到暂存区
  for file in $include_files; do
    if [ -e "$SKILL_DIR/$file" ]; then
      cp -R "$SKILL_DIR/$file" "$skill_staging_dir/"
    else
      log_warning "文件不存在，跳过: $SKILL_DIR/$file"
    fi
  done
  
  # 清理排除的文件
  find "$skill_staging_dir" -name "__pycache__" -type d -exec rm -rf {} +
  find "$skill_staging_dir" -name "*.pyc" -delete
  find "$skill_staging_dir" -name ".ruff_cache" -type d -exec rm -rf {} +
  find "$skill_staging_dir" -name ".DS_Store" -delete
  find "$skill_staging_dir" -name "node_modules" -type d -exec rm -rf {} +
  
  # 打包
  cd "$staging_dir"
  tar -czf "../$PACKAGE_NAME" "$SKILL_NAME"
  cd - > /dev/null
  
  # 清理暂存区
  rm -rf "$staging_dir"
  
  local PACKAGE_SIZE=$(du -h "$BUILD_DIR/$PACKAGE_NAME" | cut -f1)
  log_success "Skill 包已创建: $PACKAGE_SIZE"
  echo ""
}

# 验证包内容
verify_package() {
  log_step "4/7" "验证包内容"
  
  local FILE_COUNT=$(tar -tzf "$BUILD_DIR/$PACKAGE_NAME" | wc -l)
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
  
  # 从模板生成 install.js
  cat > "$INSTALLER_DIR/install.js" <<'EOF'
#!/usr/bin/env node

/**
 * __SKILL_DISPLAY_NAME__ 自动安装器
 *
 * 使用方法:
 *   npx __INSTALLER_PKG__
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const https = require("https");
const os = require("os");

const SKILL_NAME = "__SKILL_NAME__";
const SKILL_VERSION = "__SKILL_VERSION__";
const GITHUB_REPO = "__REPO_OWNER__/__REPO_NAME__";
const RELEASE_TAG = "__RELEASE_TAG__";
const PACKAGE_NAME = "__PACKAGE_NAME__";
const RELEASE_URL = `https://github.com/${GITHUB_REPO}/releases/download/${RELEASE_TAG}/${PACKAGE_NAME}`;

// 颜色输出
const colors = {
  reset: "\x1b[0m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  cyan: "\x1b[36m",
  gray: "\x1b[90m",
};

function log(message, color = "reset") {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, message) {
  log(`[${step}/6] ${message}`, "cyan");
}

function logSuccess(message) {
  log(`✅ ${message}`, "green");
}

function logError(message) {
  log(`❌ ${message}`, "red");
}

function logWarning(message) {
  log(`⚠️  ${message}`, "yellow");
}

// 检测 skills 目录
function getSkillsDir() {
  const homeDir = os.homedir();
  const skillsDir = path.join(homeDir, ".agents", "skills");

  if (!fs.existsSync(skillsDir)) {
    log("\n创建 skills 目录...", "gray");
    fs.mkdirSync(skillsDir, { recursive: true });
  }

  return skillsDir;
}

// 检查是否已安装
function checkExisting(skillsDir) {
  const skillPath = path.join(skillsDir, SKILL_NAME);

  if (fs.existsSync(skillPath)) {
    logWarning(`检测到已安装的 ${SKILL_NAME} skill`);

    const readline = require("readline").createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    return new Promise((resolve) => {
      readline.question("是否覆盖安装? [y/N]: ", (answer) => {
        readline.close();

        if (answer.toLowerCase() === "y" || answer.toLowerCase() === "yes") {
          log("正在删除旧版本...", "gray");
          fs.rmSync(skillPath, { recursive: true, force: true });
          resolve(true);
        } else {
          logError("安装已取消");
          resolve(false);
        }
      });
    });
  }

  return Promise.resolve(true);
}

// 下载并解压
function downloadAndExtract(skillsDir) {
  return new Promise((resolve, reject) => {
    const tempFile = path.join(os.tmpdir(), PACKAGE_NAME);
    const file = fs.createWriteStream(tempFile);
    let requestCompleted = false;

    log("下载 skill 包...", "gray");

    const doDownload = (url) => {
      const request = https.get(url, (response) => {
        // 检查 HTTP 状态码
        if (response.statusCode < 200 || response.statusCode >= 400) {
          file.close();
          if (fs.existsSync(tempFile)) {
            fs.unlinkSync(tempFile);
          }
          requestCompleted = true;
          reject(new Error(`下载失败: HTTP ${response.statusCode}`));
          return;
        }

        if (response.statusCode === 302 || response.statusCode === 301) {
          // 处理重定向
          if (response.headers.location) {
            doDownload(response.headers.location);
          } else {
            file.close();
            if (fs.existsSync(tempFile)) {
              fs.unlinkSync(tempFile);
            }
            requestCompleted = true;
            reject(new Error("重定向缺少 Location 头"));
          }
          return;
        }

        response.pipe(file);

        file.on("finish", () => {
          file.close();

          if (requestCompleted) return;

          try {
            log("解压文件...", "gray");
            execSync(`tar -xzf ${tempFile} -C ${skillsDir}`, {
              stdio: "inherit",
            });
            fs.unlinkSync(tempFile);
            resolve();
          } catch (error) {
            if (fs.existsSync(tempFile)) {
              fs.unlinkSync(tempFile);
            }
            reject(new Error(`解压失败: ${error.message}`));
          }
        });
      });

      // 设置 30 秒超时
      request.setTimeout(30000, () => {
        file.close();
        if (fs.existsSync(tempFile)) {
          fs.unlinkSync(tempFile);
        }
        requestCompleted = true;
        request.destroy();
        reject(new Error('下载超时 (30s)'));
      });

      request.on("error", (error) => {
        file.close();
        if (fs.existsSync(tempFile)) {
          fs.unlinkSync(tempFile);
        }
        requestCompleted = true;
        reject(new Error(`下载失败: ${error.message}`));
      });
    };

    doDownload(RELEASE_URL);
  });
}

// 验证安装
function verifyInstallation(skillsDir) {
  const skillPath = path.join(skillsDir, SKILL_NAME);
  const requiredFiles = ["SKILL.md"];

  for (const file of requiredFiles) {
    const filePath = path.join(skillPath, file);
    if (!fs.existsSync(filePath)) {
      throw new Error(`缺少必需文件: ${file}`);
    }
  }

  return skillPath;
}

// 检查系统依赖
function checkDependencies() {
  const deps = {
    python3: false,
    node: false,
  };

  try {
    execSync("python3 --version", { stdio: "pipe" });
    deps.python3 = true;
  } catch (e) {
    // Python 未安装
  }

  try {
    execSync("node --version", { stdio: "pipe" });
    deps.node = true;
  } catch (e) {
    // Node 未安装
  }

  return deps;
}

// 主安装流程
async function main() {
  console.log("\n" + "=".repeat(60));
  log("🎨 __SKILL_DISPLAY_NAME__ 安装器", "cyan");
  log(`版本: v${SKILL_VERSION}`, "gray");
  console.log("=".repeat(60) + "\n");

  try {
    // Step 1: 检查系统依赖
    logStep(1, "检查系统依赖");
    const deps = checkDependencies();

    if (deps.python3) {
      logSuccess("Python 3 已安装");
    } else {
      logWarning("Python 3 未安装（某些功能需要）");
      log("    安装方法: https://www.python.org/downloads/", "gray");
    }

    if (deps.node) {
      logSuccess("Node.js 已安装");
    } else {
      logWarning("Node.js 未安装");
      log("    安装方法: https://nodejs.org/", "gray");
    }

    console.log();

    // Step 2: 确定安装目录
    logStep(2, "确定安装目录");
    const skillsDir = getSkillsDir();
    logSuccess(`安装目录: ${skillsDir}`);
    console.log();

    // Step 3: 检查已存在的安装
    logStep(3, "检查已有安装");
    const shouldContinue = await checkExisting(skillsDir);
    if (!shouldContinue) {
      process.exit(0);
    }
    console.log();

    // Step 4: 下载并解压
    logStep(4, "下载 skill 包");
    await downloadAndExtract(skillsDir);
    logSuccess("下载完成");
    console.log();

    // Step 5: 验证安装
    logStep(5, "验证安装");
    const skillPath = verifyInstallation(skillsDir);
    logSuccess("验证通过");
    console.log();

    // Step 6: 完成
    logStep(6, "完成安装");
    logSuccess("设置完成");
    console.log();

    // 安装成功
    console.log("=".repeat(60));
    logSuccess("__SKILL_DISPLAY_NAME__ 安装成功！");
    console.log("=".repeat(60) + "\n");

    log("📍 安装位置:", "cyan");
    log(`   ${skillPath}\n`, "gray");

    log("📚 快速开始:", "cyan");
    log('   在对话中使用此 skill', "gray");
    log("   Agent 会自动调用\n", "gray");

    log("📖 查看文档:", "cyan");
    log(`   cat ${path.join(skillPath, "README.md")}\n`, "gray");

    if (!deps.python3 || !deps.node) {
      logWarning("提醒: 某些功能需要安装缺失的依赖");
    }
  } catch (error) {
    console.log();
    logError(`安装失败: ${error.message}`);
    console.log();
    log("💡 故障排除:", "yellow");
    log("   1. 检查网络连接", "gray");
    log("   2. 确认有写入权限", "gray");
    log("   3. 查看详细错误信息", "gray");
    console.log();
    process.exit(1);
  }
}

// 运行安装
if (require.main === module) {
  main();
}

module.exports = { main };
EOF

  # 替换占位符
  portable_sed_inplace "s|__SKILL_NAME__|$SKILL_NAME|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__SKILL_DISPLAY_NAME__|$SKILL_DISPLAY_NAME|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__SKILL_VERSION__|$SKILL_VERSION|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__REPO_OWNER__|$REPO_OWNER|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__REPO_NAME__|$REPO_NAME|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__RELEASE_TAG__|$RELEASE_TAG|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__PACKAGE_NAME__|$PACKAGE_NAME|g" "$INSTALLER_DIR/install.js"
  portable_sed_inplace "s|__INSTALLER_PKG__|$INSTALLER_PKG|g" "$INSTALLER_DIR/install.js"
  
  # 生成 package.json
  cat > "$INSTALLER_DIR/package.json" <<EOF
{
  "name": "$INSTALLER_PKG",
  "version": "$SKILL_VERSION",
  "description": "$SKILL_DESC",
  "main": "install.js",
  "bin": {
    "$INSTALLER_BIN": "install.js"
  },
  "scripts": {
    "test": "node install.js"
  },
  "keywords": $(jq -c ".skills.\"$SKILL_NAME\".keywords" skills.json),
  "author": {
    "name": "$AUTHOR_NAME",
    "email": "$AUTHOR_EMAIL"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/$REPO_OWNER/$REPO_NAME.git",
    "directory": "skills/$SKILL_NAME"
  },
  "bugs": {
    "url": "https://github.com/$REPO_OWNER/$REPO_NAME/issues"
  },
  "homepage": "https://github.com/$REPO_OWNER/$REPO_NAME/tree/main/skills/$SKILL_NAME"
}
EOF

  chmod +x "$INSTALLER_DIR/install.js"
  
  log_success "安装器已生成"
  echo ""
}

# 生成校验和
generate_checksum() {
  log_step "6/7" "生成校验和"
  
  cd "$BUILD_DIR"
  shasum -a 256 "$PACKAGE_NAME" > "$PACKAGE_NAME.sha256"
  local SHA256=$(cat "$PACKAGE_NAME.sha256" | cut -d' ' -f1)
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
