# Claude Skills Suite

一个为 Claude Code 提供的自定义技能集合，结合专业化 Agent 和自动化 Command，全面扩展 Claude Code 的开发能力。

## 目录

- [项目概览](#项目概览)
- [自定义 Agents（14 个）](#自定义-agents14-个)
- [自定义 Commands（16 个）](#自定义-commands16-个)
- [Skills 技能（40 个）](#skills-技能40-个)
- [skills.sh - 社区技能平台](#skillssh---社区技能平台)
- [Skill Seeker - 自动化技能生成工具](#skill-seeker---自动化技能生成工具)
- [安装](#安装)
- [在 Claude Code 中配置和使用](#在-claude-code-中配置和使用)
- [创建自定义技能](#创建自定义技能)
- [贡献](#贡献)
- [支持](#支持)
- [许可证](#许可证)

## 项目概览

```
claude-skills-suite/
├── agents/              # 14 个专业化 Agent（自动触发的子代理）
├── commands/            # 16 个自定义 Command（/slash 命令）
├── skills/              # 16 个自研 Skill（另有 24 个来自 skills.sh）
├── configs/             # 预设抓取配置（34 个框架/工具）
├── skill_seekers/       # Skill Seeker 主程序包
│   ├── cli/             # CLI 工具
│   └── mcp/             # MCP 服务实现
├── scripts/             # 辅助脚本
└── *.sh                 # MCP 服务管理脚本
```

---

## 自定义 Agents（14 个）

Agents 是专业化的子代理，由 Claude Code 在对话中根据任务需求**自动触发**。安装后无需手动调用，Claude 会在合适的时机自动分配任务给对应的 Agent。

> 配置路径：`agents/`

### 开发与架构

| Agent | 说明 |
|-------|------|
| **architect** | 软件架构专家，负责系统设计、可扩展性分析和技术决策 |
| **planner** | 规划专家，为复杂功能和重构创建全面、可执行的实施计划 |
| **build-error-resolver** | 构建和 TypeScript 错误修复专家，以最小改动快速修复编译错误 |
| **vue3-frontend-developer** | Vue3 高级前端工程师，专精 Vue3 + TypeScript + Tailwind CSS 开发 |

### 代码质量与测试

| Agent | 说明 |
|-------|------|
| **code-reviewer** | 代码审查专家，审查代码质量、安全性和可维护性 |
| **tdd-guide** | 测试驱动开发（TDD）专家，强制先写测试后实现的工作流，确保 80%+ 覆盖率 |
| **e2e-runner** | 端到端测试专家，使用 Vercel Agent Browser（优先）和 Playwright 管理测试 |
| **refactor-cleaner** | 死代码清理和代码整合专家，安全移除未使用代码和重复逻辑 |

### 安全与数据库

| Agent | 说明 |
|-------|------|
| **security-reviewer** | 安全漏洞检测和修复专家，聚焦 OWASP Top 10 |
| **postgre-database-reviewer** | PostgreSQL 数据库专家，负责查询优化、Schema 设计和性能调优 |
| **mysql-database-reviewer** | MySQL 数据库专家，负责查询优化、Schema 设计和性能调优 |

### 产品与文档

| Agent | 说明 |
|-------|------|
| **product-manager** | 产品经理，专注需求发现和 PRD 文档编写 |
| **ui-ux-designer** | 高级 UI/UX 设计师，将需求转化为设计规范和视觉指南 |
| **doc-updater** | 文档和 Codemap 专家，负责更新架构文档并保持文档与代码同步 |

---

## 自定义 Commands（16 个）

Commands 是通过 `/command` 方式调用的自动化工作流。在 Claude Code 对话中输入对应的斜杠命令即可触发。

> 配置路径：`commands/`

### 规划与工作流

| 命令 | 说明 |
|------|------|
| `/plan` | 重述需求、评估风险并创建分步实施计划，等待用户确认后再执行 |
| `/orchestrate` | 顺序编排多个 Agent 完成复杂任务（feature、bugfix、refactor、security） |
| `/checkpoint` | 创建、验证和列出工作流检查点，跟踪进度并对比代码变更 |
| `/eval` | 定义、检查和报告 Eval 标准，管理评估驱动开发工作流 |

### 代码质量与审查

| 命令 | 说明 |
|------|------|
| `/pre-commit-review` | 对未提交的变更进行全面的安全和质量审查 |
| `/full-review` | 编排 code-reviewer、security-auditor 和 test-writer 进行综合代码审查 |
| `/refactor-clean` | 识别并安全移除死代码，通过测试验证安全性 |

### 测试

| 命令 | 说明 |
|------|------|
| `/tdd` | 强制执行 TDD 工作流：先写测试接口、再生成测试、最后实现最小代码 |
| `/test-coverage` | 分析测试覆盖率并生成缺失的测试，目标达到 80%+ 覆盖率 |
| `/e2e` | 生成并运行 Playwright 端到端测试，捕获截图/视频/Trace |

### 构建与修复

| 命令 | 说明 |
|------|------|
| `/ts-build-fix` | 逐一增量修复 TypeScript 和构建错误 |
| `/verify` | 运行全面验证（构建、类型检查、Lint、测试、日志、Git 状态） |

### 文档与学习

| 命令 | 说明 |
|------|------|
| `/update-codemaps` | 分析代码库结构并更新架构文档 |
| `/update-docs` | 从 source-of-truth（package.json、.env.example）同步文档 |
| `/learn` | 从当前会话提取可复用模式并保存为可复用技能 |

### 工具

| 命令 | 说明 |
|------|------|
| `/setup-pm` | 配置项目首选包管理器（npm/pnpm/yarn/bun） |

---

## Skills 技能（40 个）

Skills 是提供领域知识和工具包的模块化技能。Claude 会根据用户任务描述**自动识别并加载**合适的技能。

本项目包含 16 个自研技能（`skills/` 目录），另有 24 个来自 [skills.sh](https://skills.sh/) 社区平台的优质技能。

### 自研技能（16 个）

> 配置路径：`skills/`

#### 前端与可视化

| 技能 | 说明 |
|------|------|
| **d3js** | 使用 D3.js 创建交互式数据可视化（图表、网络图、地理可视化等） |
| **ui-ux-pro-max** | UI/UX 设计智能，提供 50 种风格、21 个配色方案、50 组字体搭配，支持 9 个技术栈 |
| **agent-brower** | 浏览器自动化交互，用于网页测试、表单填写、截图和数据提取 |

#### 后端与数据库

| 技能 | 说明 |
|------|------|
| **backend-patterns** | 后端架构模式，包括 API 设计、数据库优化（Node.js、Express、NestJS、FastAPI） |
| **postgres-patterns** | PostgreSQL 数据库模式，查询优化、Schema 设计、索引和安全最佳实践 |
| **mysql-patterns** | MySQL 数据库模式，查询优化、Schema 设计、索引和安全 |
| **sequelize-patterns** | Sequelize ORM 模式，支持 PostgreSQL、MySQL、SQLite 等多种数据库 |

#### 小程序开发

| 技能 | 说明 |
|------|------|
| **wechat-miniprogram** | 微信小程序开发框架（WXML、WXSS、WXS、组件开发、微信 API） |
| **tdesign-miniprogram** | 腾讯 TDesign 小程序 UI 组件库，用于构建微信小程序界面 |

#### 开发工作流

| 技能 | 说明 |
|------|------|
| **tdd-workflow** | 测试驱动开发工作流，强制先写测试，确保 80%+ 覆盖率 |
| **security-review** | 安全审查清单和模式，用于认证、用户输入、API 端点等场景 |
| **continuous-learning-v2** | 基于直觉的学习系统，通过 Hooks 观察会话并演化为技能/命令/Agent |
| **iterative-retrieval** | 渐进式上下文检索模式，解决子代理上下文传递问题 |

#### 数据处理

| 技能 | 说明 |
|------|------|
| **process-faq** | 将 FAQ 文档（xlsx、word、pdf、txt）转换为 RAG 优化的结构化格式 |

#### AI Agent 开发

| 技能 | 说明 |
|------|------|
| **deepagents** | LangChain Deep Agents 框架，用于构建自主编码 Agent |

#### 其他

| 技能 | 说明 |
|------|------|
| **verification-loop** | Claude Code 会话的全面验证系统 |

### 社区技能（24 个，来自 skills.sh）

以下技能通过 [skills.sh](https://skills.sh/) 平台安装，安装后位于 `~/.claude/skills/`。

#### 前端与设计

| 技能 | 说明 |
|------|------|
| **frontend-design** | 创建独特的、生产级前端界面，具备高设计质量 |
| **vue-best-practices** | Vue.js 最佳实践，强制使用 Composition API + TypeScript |
| **vant-vue3** | Vant Vue 3 移动端组件库指南，包括主题和最佳实践 |
| **web-design-guidelines** | 审查 UI 代码是否符合 Web 界面设计规范和无障碍标准 |
| **canvas-design** | 使用设计哲学创建精美的 .png 和 .pdf 视觉艺术 |
| **algorithmic-art** | 使用 p5.js 创建算法艺术，支持种子随机和交互式参数探索 |
| **theme-factory** | 为幻灯片、文档、报告、HTML 页面等应用预设或自定义主题 |
| **slack-gif-creator** | 创建针对 Slack 优化的动画 GIF，提供约束验证工具 |
| **remotion-best-practices** | Remotion 最佳实践 - 使用 React 创建视频 |

#### 后端框架

| 技能 | 说明 |
|------|------|
| **fastapi-templates** | 创建生产级 FastAPI 项目，包含异步模式、依赖注入和错误处理 |
| **nestjs-best-practices** | NestJS 最佳实践和架构模式，构建生产级应用 |
| **langchain-architecture** | 使用 LangChain 1.x 和 LangGraph 设计 LLM 应用 |
| **sqlalchemy-orm** | SQLAlchemy Python SQL 工具包和 ORM，含 Alembic 迁移 |

#### 文档与办公

| 技能 | 说明 |
|------|------|
| **pdf** | PDF 操作工具包（提取文本/表格、创建、合并/拆分、表单处理） |
| **docx** | Word 文档创建、编辑和分析，支持修订追踪、批注和格式保留 |
| **pptx** | PowerPoint 演示文稿创建、编辑和分析 |
| **xlsx** | Excel 电子表格创建、编辑和分析，支持公式、格式和数据可视化 |

#### 测试与自动化

| 技能 | 说明 |
|------|------|
| **playwright-skill** | 基于 Playwright 的完整浏览器自动化，测试页面、填写表单、截图 |
| **webapp-testing** | 使用 Playwright 交互和测试本地 Web 应用，支持截图和日志捕获 |

#### 开发工具

| 技能 | 说明 |
|------|------|
| **mcp-builder** | 创建高质量 MCP 服务器的指南，让 LLM 与外部服务交互 |
| **skill-creator** | 创建有效技能的指南，扩展 Claude 的知识和工具集成能力 |
| **find-skills** | 帮助用户发现和安装 Agent 技能，回答"有没有能做 X 的技能" |
| **planning-with-files** | Manus 风格的基于文件的任务规划，支持 `/clear` 后自动恢复会话 |

#### 产品管理

| 技能 | 说明 |
|------|------|
| **product-manager-toolkit** | 产品经理工具包（RICE 优先级、用户访谈分析、PRD 模板、GTM 策略） |

---

## skills.sh - 社区技能平台

[skills.sh](https://skills.sh/) 是由 **Vercel** 打造的开放式 AI Agent 技能生态系统，提供超过 50,000 个可复用技能，兼容 20+ AI 代理（Claude Code、Cursor、GitHub Copilot、VSCode 等）。

### 安装技能

```bash
# 从 skills.sh 安装技能（一键安装）
npx skills add <owner/skill-name>

# 示例
npx skills add anthropic/mcp-builder
npx skills add vercel/frontend-design
```

### 发现技能

- 访问 [skills.sh](https://skills.sh/) 浏览和搜索技能
- 支持按**全时段热门**、**24 小时趋势**、**最热**排序
- 每个技能显示安装次数，方便评估热门程度
- 安装 `find-skills` 技能后，可在 Claude Code 中直接询问"有没有能做 X 的技能"，自动搜索并安装

### 发布技能

将你的技能发布到 skills.sh 社区，让其他开发者也能使用：

```bash
npx skills publish
```

---

## Skill Seeker - 自动化技能生成工具

Skill Seeker 是一款强大的自动化工具，能够将文档网站、GitHub 仓库和 PDF 文件转化为可直接投入生产的 Claude AI 技能。

> **项目来源**：[Skill Seekers GitHub 仓库](https://github.com/yusufkaraaslan/Skill_Seekers)
> 本项目集成了 Skill Seeker 工具，用于自动化生成 Claude 技能。

### 主要特性

- **多源抓取**：支持文档网站、GitHub 仓库和 PDF 文件
- **智能处理**：自动提取、清洗和优化内容
- **配置管理**：内置 34 个预设配置（React、Django、FastAPI、Kubernetes 等）
- **自动化流程**：一键生成完整的 Claude 技能包
- **MCP 集成**：通过 Model Context Protocol 无缝集成到 AI 代理中

### 快速开始

#### 1. 一次性设置（需要约 5 分钟）

在命令行中运行：

```bash
./skill_seeker_setup_mcp.sh
```

该脚本会自动：

- 检测你的 Python 环境
- 安装必要的依赖（mcp、fastmcp、requests、beautifulsoup4、uvicorn）
- 检测已安装的 AI 代理（Claude Code、Cursor、Windsurf 等）
- 自动配置 MCP 服务器
- 启动 HTTP 服务器（如需要）

#### 服务管理脚本

项目提供三个脚本来管理 MCP 服务：

| 脚本                        | 用途     | 何时使用           |
| --------------------------- | -------- | ------------------ |
| `skill_seeker_setup_mcp.sh` | 安装配置 | 首次安装或重新配置 |
| `skill_seeker_start_mcp.sh` | 启动服务 | 日常启动 HTTP 服务 |
| `skill_seeker_stop_mcp.sh`  | 停止服务 | 停止运行中的服务   |

**启动服务：**

```bash
# 默认启动（后台运行，端口 3000）
./skill_seeker_start_mcp.sh

# 指定端口
./skill_seeker_start_mcp.sh -p 8080

# 前台运行（方便调试，Ctrl+C 停止）
./skill_seeker_start_mcp.sh -f

# 查看帮助
./skill_seeker_start_mcp.sh -h
```

**停止服务：**

```bash
./skill_seeker_stop_mcp.sh
```

#### 2. 使用 Skill Seeker

设置完成后，在 Claude Code 中直接询问：

```
# 从文档网站生成技能
"从 https://react.dev/ 生成一个 React 技能"

# 从 PDF 生成技能
"抓取 docs/manual.pdf 并创建技能"

# 从 GitHub 仓库生成技能
"从 GitHub 仓库 https://github.com/user/repo 生成技能"

# 列出所有可用的预设配置
"列出所有可用的配置"

# 验证配置文件
"验证 configs/react.json"

# 估算页面数量
"估算 configs/godot.json 的页面数"
```

### 可用的 MCP 工具（17 个）

**配置工具：**

- `generate_config` - 为任何文档站点创建配置文件
- `list_configs` - 显示所有可用的预设配置
- `validate_config` - 验证配置文件结构

**抓取工具：**

- `estimate_pages` - 在抓取前估算页面数
- `scrape_docs` - 抓取文档并构建技能
- `scrape_github` - 抓取 GitHub 仓库
- `scrape_pdf` - 从 PDF 文件提取内容

**打包工具：**

- `package_skill` - 将技能打包为 .zip 文件
- `upload_skill` - 上传技能到 Claude
- `install_skill` - 安装已上传的技能

**拆分工具：**

- `split_config` - 拆分大型文档配置
- `generate_router` - 生成路由/中枢技能

**配置源工具：**

- `fetch_config` - 从远程源下载配置
- `submit_config` - 提交配置到社区
- `add_config_source` - 添加自定义配置源
- `list_config_sources` - 显示可用的配置源
- `remove_config_source` - 移除配置源

### 预设配置

Skill Seeker 内置了 34 个流行框架和工具的配置：

- **Web 框架**：React、Vue、Astro、Django、Laravel、FastAPI、NestJS、Hono
- **ORM / 数据库**：Sequelize、SQLAlchemy
- **AI / Agent**：LangChain、LangGraph、DeepAgents
- **小程序**：微信小程序、TDesign 小程序、Vant
- **DevOps**：Kubernetes、Ansible
- **游戏开发**：Godot
- **样式**：Tailwind CSS
- **工具**：Claude Code

查看 [configs/](configs/) 目录了解所有可用配置。

### 工作原理

1. **配置生成/选择**：使用预设配置或为新文档站点生成配置
2. **内容抓取**：从网站、GitHub 或 PDF 提取内容
3. **内容处理**：清洗、优化和结构化内容
4. **技能生成**：创建符合 Claude Code 标准的技能包
5. **安装部署**：自动安装到 Claude Code

### 高级功能

#### HTTP 传输支持

对于需要 HTTP 传输的 AI 代理（如 Cursor、Windsurf），Skill Seeker 可以运行 HTTP 模式：

```bash
# 推荐：使用启动脚本
./skill_seeker_start_mcp.sh -p 3000

# 或手动运行
python3 -m skill_seekers.mcp.server_fastmcp --http --port 3000
```

服务启动后会生成以下文件（在项目根目录）：

| 文件               | 说明             |
| ------------------ | ---------------- |
| `.mcp-server.pid`  | 存储服务进程 PID |
| `.mcp-server.port` | 存储服务端口号   |
| `.mcp-server.log`  | 服务日志输出     |

#### 自定义配置

你可以创建自定义配置文件来抓取任何文档站点：

```json
{
  "name": "my-framework",
  "base_url": "https://docs.myframework.com",
  "start_urls": ["/getting-started", "/api-reference"],
  "max_pages": 100,
  "skill_name": "my-framework-skill"
}
```

然后使用：

```
"使用 configs/my-config.json 生成技能"
```

### 故障排除

**Python 环境问题：**

- 确保 Python 3.10+ 已安装
- 建议使用虚拟环境

**MCP 服务器问题：**

- 检查服务器日志：`tail -f .mcp-server.log`
- 测试连接：`curl http://127.0.0.1:3000/health`
- 检查服务状态：`cat .mcp-server.pid`
- 停止服务：`./skill_seeker_stop_mcp.sh`

**代理配置问题：**

- 查看代理日志（Claude Code: `~/Library/Logs/Claude Code/`）
- 验证配置文件语法：`jq empty ~/.config/claude-code/mcp.json`

更多信息请参考安装脚本输出的详细说明。

---

## 安装

### 前置要求

- Python 3.10 或更高版本（Skill Seeker 需要）
- Node.js 和 npm（用于 `npx skills` 命令和部分技能）
- Claude Code CLI 工具

### Claude Code 扩展目录说明

Claude Code 支持两级目录，**项目级优先于全局级**：

| 类型 | 全局目录（所有项目生效） | 项目级目录（仅当前项目生效） |
|------|--------------------------|------------------------------|
| Agents | `~/.claude/agents/` | `<项目>/.claude/agents/` |
| Commands | `~/.claude/commands/` | `<项目>/.claude/commands/` |
| Skills | `~/.claude/skills/` | `<项目>/.claude/skills/` |

### 方式一：全局安装（推荐，所有项目可用）

```bash
# 1. 克隆仓库
git clone https://github.com/jone_qian/claude-skills-suite.git
cd claude-skills-suite

# 2. 创建目录（如不存在）
mkdir -p ~/.claude/agents ~/.claude/commands ~/.claude/skills

# 3. 安装 Agents（14 个专业子代理）
cp agents/*.md ~/.claude/agents/

# 4. 安装 Commands（16 个 /slash 命令）
cp commands/*.md ~/.claude/commands/

# 5. 安装自研 Skills（16 个技能包）
cp -r skills/* ~/.claude/skills/

# 6. 重启 Claude Code 生效
```

### 方式二：项目级安装（仅当前项目可用）

```bash
# 在你的项目根目录下执行
cd /path/to/your-project

# 创建目录
mkdir -p .claude/agents .claude/commands .claude/skills

# 按需安装（路径替换为 claude-skills-suite 所在位置）
cp /path/to/claude-skills-suite/agents/*.md .claude/agents/
cp /path/to/claude-skills-suite/commands/*.md .claude/commands/
cp -r /path/to/claude-skills-suite/skills/* .claude/skills/
```

### 方式三：从 skills.sh 安装社区技能

```bash
# 安装单个技能（自动安装到 ~/.claude/skills/）
npx skills add anthropic/mcp-builder
npx skills add vercel/frontend-design

# 安装 find-skills 后，可在 Claude Code 中搜索和安装技能
npx skills add punkpeye/find-skills
```

### （可选）安装 Skill Seeker

如果你想从文档网站、GitHub 仓库或 PDF 自动生成技能：

```bash
./skill_seeker_setup_mcp.sh
```

### 验证安装

重启 Claude Code 后测试：

```
# 测试 Commands
/plan 创建一个用户认证模块

# 测试 Agents（自动触发，无需手动调用）
"帮我审查这段代码的安全性"

# 测试 Skills（自动识别加载）
"用 D3.js 创建一个交互式柱状图"
```

---

## 在 Claude Code 中配置和使用

### 三种扩展类型对比

| 类型 | 存放目录 | 触发方式 | 用途 |
|------|----------|----------|------|
| **Agents** | `.claude/agents/` | Claude 自动分配任务 | 专业化子代理，处理特定领域任务 |
| **Commands** | `.claude/commands/` | 用户输入 `/command` | 自动化工作流，一键执行复杂流程 |
| **Skills** | `.claude/skills/` | Claude 自动识别加载 | 领域知识和工具包 |

### 配置文件格式

**Agent（`.md` 文件）：** 定义专业化子代理的行为和能力。

**Command（`.md` 文件）：** 定义 `/slash` 命令的执行逻辑。

**Skill（`SKILL.md` 文件）：** 需要 YAML 前置元数据：

```markdown
---
name: skill-name
description: 技能的简短描述，说明何时使用此技能
tools: Read, Write, Bash, AskUserQuestion
---

# 技能名称

技能的详细文档...
```

### 优先级规则

1. **项目级配置**（`.claude/`）优先于**全局配置**（`~/.claude/`）
2. Claude 会根据 `description` 字段选择最匹配的技能
3. 你可以明确指定要使用的技能或命令

---

## 创建自定义技能

### 使用 Skill Seeker 创建

最简单的方法是使用 Skill Seeker 从现有文档生成技能：

```
"从 https://docs.example.com 生成一个技能"
```

### 手动创建

想要创建自定义技能？请参阅 [Claude Code Skills 文档](https://github.com/anthropics/claude-code)。

每个技能应该包含：

- `SKILL.md` - 带有 YAML 前置元数据的技能定义
- 支持脚本和文件（如需要）
- `requirements.txt` 或 `package.json` - 依赖（如需要）

### 技能目录结构示例

```
my-custom-skill/
├── SKILL.md              # 必需：技能定义
├── requirements.txt      # 如果是 Python 项目
├── package.json          # 如果是 Node.js 项目
├── scripts/              # 辅助脚本
│   ├── process.py
│   └── analyze.js
└── templates/            # 模板文件
    └── output.template
```

---

## 贡献

欢迎贡献！添加新 Agent / Command / Skill 的步骤：

1. Fork 此仓库
2. 在对应目录（`agents/`、`commands/`、`skills/`）下创建新文件
3. 添加文档和示例
4. 提交 pull request

### 贡献指南

- Agent / Command 为单个 `.md` 文件，Skill 需要包含 `SKILL.md`
- 提供使用示例
- 遵循现有文件的命名和结构约定
- 更新 README.md 添加新内容的信息

---

## 支持

遇到问题或有疑问：

- 在 GitHub 上提交 issue
- 查看各个 Agent / Command / Skill 的文档
- 询问 Claude 寻求帮助

### 常见问题

**Q: Agent / Skill 没有被 Claude 识别？**
A: 确保文件在 `~/.claude/agents/`、`~/.claude/skills/` 或项目的 `.claude/` 对应子目录中。

**Q: 如何更新？**
A: 运行 `git pull` 更新仓库，然后重新复制到 Claude 目录。

**Q: 如何禁用某个 Agent / Skill？**
A: 从对应目录中移除该文件即可。

---

## 许可证

MIT License - 欢迎自由使用和修改。

---

## 关于

此技能套件由社区维护，旨在扩展 Claude Code 在常见开发任务中的能力。

**项目维护者**：jone_qian
**仓库地址**：https://github.com/jone_qian/claude-skills-suite

---

## 资源链接

- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Skill Seekers 原始仓库](https://github.com/yusufkaraaslan/Skill_Seekers) - 自动化技能生成工具
- [预设配置文件](configs/)
- [问题追踪](https://github.com/jone_qian/claude-skills-suite/issues)
