# Makefile for Agent Skills
# 使用方法:
#   make <target>
#   make help  # 查看所有可用命令

.PHONY: help init validate validate-all preview tag release lint format

# 默认目标
.DEFAULT_GOAL := help

# 颜色定义
GREEN  := \033[0;32m
YELLOW := \033[1;33m
CYAN   := \033[0;36m
NC     := \033[0m

# ==============================================================================
# 帮助命令
# ==============================================================================

help: ## 显示所有可用命令
	@echo ""
	@echo "$(CYAN)Agent Skills - 可用命令$(NC)"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "示例:"
	@echo "  make validate              # 验证所有 skills"
	@echo "  make validate mermaid      # 验证单个 skill"
	@echo "  make tag mermaid 1.0.0   # 为 skill 打标"
	@echo ""

# ==============================================================================
# 初始化命令
# ==============================================================================

init: ## 初始化仓库
	@echo "$(CYAN)[初始化]$(NC) 运行 init.sh..."
	@./scripts/init.sh

# ==============================================================================
# 创建 Skill 命令
# ==============================================================================

create: ## 创建新 Skill (用法: make create SKILL_NAME=mermaid)
	@if [ -z "$(SKILL_NAME)" ]; then \
		echo "$(YELLOW)错误: 请指定 SKILL_NAME$(NC)"; \
		echo "示例: make create SKILL_NAME=my-new-skill"; \
		exit 1; \
	fi
	@echo "$(CYAN)[创建]$(NC) 创建 Skill: $(SKILL_NAME)..."
	@./scripts/create_skill.sh $(SKILL_NAME)

# ==============================================================================
# 验证命令
# ==============================================================================

validate: ## 验证 Skill (用法: make validate [SKILL_NAME])
	@echo "$(CYAN)[验证]$(NC) 运行验证..."
	@if [ -z "$(SKILL_NAME)" ]; then \
		./scripts/validate_skill.sh; \
	else \
		./scripts/validate_skill.sh $(SKILL_NAME); \
	fi

validate-all: ## 验证所有 Skills
	@echo "$(CYAN)[验证]$(NC) 验证所有 skills..."
	@./scripts/validate_skill.sh

# ==============================================================================
# 预览命令
# ==============================================================================

preview: ## 预览 Skill (用法: make preview [SKILL_NAME])
	@echo "$(CYAN)[预览]$(NC) 运行预览..."
	@if [ -z "$(SKILL_NAME)" ]; then \
		./scripts/preview_skill.sh; \
	else \
		./scripts/preview_skill.sh $(SKILL_NAME); \
	fi

preview-all: ## 列出所有 Skills
	@echo "$(CYAN)[预览]$(NC) 列出所有 skills..."
	@./scripts/preview_skill.sh

# ==============================================================================
# 发布命令
# ==============================================================================

tag: ## 为 Skill 打标 (用法: make tag SKILL_NAME=mermaid VERSION=1.0.0)
	@if [ -z "$(SKILL_NAME)" ]; then \
		echo "$(YELLOW)错误: 请指定 SKILL_NAME$(NC)"; \
		echo "示例: make tag SKILL_NAME=mermaid VERSION=1.0.0"; \
		exit 1; \
	fi
	@if [ -z "$(VERSION)" ]; then \
		echo "$(YELLOW)错误: 请指定 VERSION$(NC)"; \
		echo "示例: make tag SKILL_NAME=mermaid VERSION=1.0.0"; \
		exit 1; \
	fi
	@echo "$(CYAN)[发布]$(NC) 为 Skill 打标: $(SKILL_NAME) v$(VERSION)..."
	@./scripts/tag_skill.sh $(SKILL_NAME) $(VERSION)

tag-all: ## 批量为所有 Skills 打标
	@echo "$(YELLOW)警告: 将为所有 skills 打标$(NC)"
	@./scripts/tag_skill.sh --all

# ==============================================================================
# 代码检查命令
# ==============================================================================

lint: ## 运行代码检查
	@echo "$(CYAN)[Lint]$(NC) 运行代码检查..."
	@command -v ruff >/dev/null 2>&1 && echo "$(GREEN)✓ Python Lint (Ruff)$(NC)" && ruff check . || echo "$(YELLOW)⚠ Ruff 未安装，跳过 Python Lint$(NC)"
	@command -v shellcheck >/dev/null 2>&1 && echo "$(GREEN)✓ Bash Lint (Shellcheck)$(NC)" && shellcheck scripts/*.sh || echo "$(YELLOW)⚠ Shellcheck 未安装，跳过 Bash Lint$(NC)"

lint-fix: ## 自动修复代码问题
	@echo "$(CYAN)[Lint Fix]$(NC) 自动修复代码问题..."
	@command -v ruff >/dev/null 2>&1 && ruff check --fix . || echo "$(YELLOW)⚠ Ruff 未安装，跳过$(NC)"

# ==============================================================================
# Git 命令
# ==============================================================================

status: ## 显示 Git 状态
	@echo "$(CYAN)[Git Status]$(NC)"
	@git status --short

log: ## 显示 Git 日志
	@echo "$(CYAN)[Git Log]$(NC)"
	@git log --oneline -10

commit: ## 提交更改 (用法: make commit MESSAGE="feat: add new skill")
	@if [ -z "$(MESSAGE)" ]; then \
		echo "$(YELLOW)错误: 请指定 MESSAGE$(NC)"; \
		echo "示例: make commit MESSAGE=\"feat(mermaid): add new feature\""; \
		exit 1; \
	fi
	@echo "$(CYAN)[Git]$(NC) 添加并提交更改..."
	@git add .
	@git commit -m "$(MESSAGE)"

push: ## 推送到远程仓库
	@echo "$(CYAN)[Git]$(NC) 推送到远程仓库..."
	@git push

push-tags: ## 推送所有 Tags
	@echo "$(CYAN)[Git]$(NC) 推送所有 tags..."
	@git push origin --tags

# ==============================================================================
# 快速命令组合
# ==============================================================================

dev: validate preview-all ## 开发验证：验证 + 预览

publish: validate tag ## 完整发布流程：验证 + 打标 (包含推送)

# ==============================================================================
# 清理命令
# ==============================================================================

clean: ## 清理临时文件
	@echo "$(CYAN)[清理]$(NC) 清理临时文件..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ 清理完成$(NC)"

# ==============================================================================
# 信息命令
# ==============================================================================

info: ## 显示项目信息
	@echo ""
	@echo "$(CYAN)Agent Skills 项目信息$(NC)"
	@echo "=================================="
	@echo "Skills 数量: $(shell jq -r '.skills | length' skills.json)"
	@echo "Git 仓库: $(shell git remote get-url origin 2>/dev/null || echo '未配置')"
	@echo "当前分支: $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '未知')"
	@echo "最近提交: $(shell git log -1 --oneline 2>/dev/null || echo '无')"
	@echo ""
