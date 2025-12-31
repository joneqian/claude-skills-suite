# Claude Skills Suite

一个为 Claude Code 提供的自定义技能集合，用于扩展其功能。

## 目录

- [可用技能](#可用技能)
- [Skill Seeker - 自动化技能生成工具](#skill-seeker---自动化技能生成工具)
- [安装](#安装)
- [在 Claude Code 中配置和使用 Skill](#在-claude-code-中配置和使用-skill)
- [创建自定义技能](#创建自定义技能)
- [贡献](#贡献)
- [支持](#支持)
- [许可证](#许可证)

## 可用技能

### process-faq

将原始 FAQ 文档转换为 RAG 优化的结构化格式。

**功能特性：**
- 支持多种格式的 FAQ 文档分析（Excel、Word、PDF、文本）
- 识别结构和内容质量问题
- 自动生成分类和关键词
- 去除重复并合并相似问题
- 输出标准化的 Excel 格式供 RAG 系统使用

**使用场景：**
- 知识库准备
- 客服 FAQ 组织整理
- RAG 系统数据准备
- FAQ 质量改进

**使用示例：**
```
用户：处理我的 FAQ.xlsx 并转换为 RAG 格式

用户：分析这个客服文档并重新组织为 RAG 格式

用户：我有一个包含 FAQ 的 Word 文档，能帮我整理一下吗？
```

Claude 会自动使用该技能帮助你完成任务。

[查看详细文档 →](output/process-faq/SKILL.md)

---

### playwright-skill

完整的浏览器自动化测试工具，基于 Playwright。

**功能特性：**
- 自动检测开发服务器
- 编写干净的测试脚本到 /tmp 目录
- 测试页面功能
- 填写表单
- 截图
- 检查响应式设计
- 验证用户体验
- 测试登录流程
- 检查链接
- 自动化任何浏览器任务

**使用场景：**
- 网站功能测试
- 浏览器交互自动化
- Web 功能验证
- 任何基于浏览器的测试任务

**使用示例：**
```
用户：测试营销页面是否美观

Claude：我会在多个视口测试营销页面。首先检测运行中的服务器...
[运行：detectDevServers()]
[输出：在端口 3001 发现服务器]
我发现你的开发服务器运行在 http://localhost:3001

[编写自定义自动化脚本到 /tmp/playwright-test-marketing.js，URL 参数化]
[运行：cd $SKILL_DIR && node run.js /tmp/playwright-test-marketing.js]
[显示结果和 /tmp/ 中的截图]
```

```
用户：检查登录是否正确重定向

Claude：我会测试登录流程。首先检查运行中的服务器...
[运行：detectDevServers()]
[输出：在端口 3000 和 3001 发现服务器]
我发现了 2 个开发服务器。应该测试哪一个？
- http://localhost:3000
- http://localhost:3001

用户：使用 3001

[编写登录自动化到 /tmp/playwright-test-login.js]
[运行：cd $SKILL_DIR && node run.js /tmp/playwright-test-login.js]
[报告：✅ 登录成功，重定向到 /dashboard]
```

**关键特性：**
- 自动检测本地开发服务器
- 默认使用可见浏览器模式便于调试
- 测试文件写入 /tmp 自动清理
- 支持响应式设计测试
- 提供表单填写和提交
- 链接检查功能
- 完整的浏览器交互能力

[查看详细文档 →](output/playwright-skill/SKILL.md)

---

### d3-viz

使用 D3.js 创建交互式数据可视化。

**功能特性：**
- 自定义图表和图形
- 网络图和层次结构可视化
- 地理可视化
- 复杂的交互行为（平移、缩放、刷选）
- 平滑的过渡动画
- 精细的样式控制
- 支持各种 JavaScript 环境（React、Vue、Svelte、原生 JS）

**适用场景：**
- 需要独特视觉编码或布局的自定义可视化
- 具有复杂交互的数据探索
- 网络/图可视化（力导向布局、树图、层次结构、弦图）
- 带自定义投影的地理可视化
- 需要平滑、编排过渡的可视化
- 出版级质量图形
- 标准库中没有的新颖图表类型

**支持的可视化类型：**
- 柱状图
- 折线图
- 散点图
- 弦图
- 热力图
- 饼图
- 力导向网络图

**使用示例：**
```javascript
// 创建响应式条形图
import * as d3 from 'd3';

function drawBarChart(data, svgElement) {
  const svg = d3.select(svgElement);

  // 设置尺寸和边距
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const width = 800 - margin.left - margin.right;
  const height = 400 - margin.top - margin.bottom;

  // 创建比例尺
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, width])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([height, 0]);

  // 绘制图表...
}
```

**核心功能：**
- 支持多种比例尺类型（线性、对数、时间、序数等）
- 丰富的交互能力（工具提示、缩放、点击）
- 平滑的过渡和动画效果
- 响应式设计支持
- 可访问性增强

[查看详细文档 →](output/d3js/SKILL.md)

---

## Skill Seeker - 自动化技能生成工具

Skill Seeker 是一款强大的自动化工具，能够将文档网站、GitHub 仓库和 PDF 文件转化为可直接投入生产的 Claude AI 技能。

### 主要特性

- **多源抓取**：支持文档网站、GitHub 仓库和 PDF 文件
- **智能处理**：自动提取、清洗和优化内容
- **配置管理**：内置多个预设配置（React、Django、FastAPI、Kubernetes 等）
- **自动化流程**：一键生成完整的 Claude 技能包
- **MCP 集成**：通过 Model Context Protocol 无缝集成到 AI 代理中

### 快速开始

#### 1. 一次性设置（需要约 5 分钟）

在 Claude Code 中，直接询问：

```
运行 skill_seeker_setup_mcp.sh
```

该脚本会自动：
- 检测你的 Python 环境
- 安装必要的依赖（mcp、fastmcp、requests、beautifulsoup4、uvicorn）
- 检测已安装的 AI 代理（Claude Code、Cursor、Windsurf 等）
- 自动配置 MCP 服务器
- 启动 HTTP 服务器（如需要）

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

Skill Seeker 内置了多个流行框架和工具的配置：

- **Web 框架**：React、Vue、Astro、Django、Laravel、FastAPI
- **DevOps**：Kubernetes、Ansible
- **游戏开发**：Godot
- **样式**：Tailwind CSS
- 更多配置持续添加中...

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
python3 -m skill_seekers.mcp.server_fastmcp --http --port 3000
```

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
- 检查服务器日志：`tail -f /tmp/skill-seekers-mcp.log`
- 测试连接：`curl http://127.0.0.1:3000/health`

**代理配置问题：**
- 查看代理日志（Claude Code: `~/Library/Logs/Claude Code/`）
- 验证配置文件语法：`jq empty ~/.config/claude-code/mcp.json`

更多信息请参考安装脚本输出的详细说明。

---

## 安装

### 前置要求

- Python 3.10 或更高版本
- Node.js 和 npm（用于某些技能）
- Claude Code CLI 工具

### 安装 Skill Seeker（推荐）

如果你想使用 Skill Seeker 自动生成技能，请先运行设置脚本：

```bash
# 在 Claude Code 中直接询问：
运行 skill_seeker_setup_mcp.sh
```

该脚本会自动处理所有配置。

### 手动安装技能

1. 克隆此仓库：
```bash
git clone https://github.com/jone_qian/claude-skills-suite.git
cd claude-skills-suite
```

2. 为你想使用的技能安装依赖：
```bash
# 对于 process-faq
pip install -r output/process-faq/requirements.txt

# 对于 playwright-skill
cd output/playwright-skill && npm run setup
```

3. 将技能复制到 Claude 的技能目录：
```bash
# 个人使用
cp -r output/process-faq ~/.claude/skills/
cp -r output/playwright-skill ~/.claude/skills/
cp -r output/d3js ~/.claude/skills/

# 项目特定使用
mkdir -p .claude/skills
cp -r output/process-faq .claude/skills/
cp -r output/playwright-skill .claude/skills/
cp -r output/d3js .claude/skills/
```

4. 重启 Claude Code

### 验证安装

启动 Claude Code 并询问：
```
可用的技能有哪些？
```

你应该能看到已安装的技能列表。

---

## 在 Claude Code 中配置和使用 Skill

### 技能目录结构

Claude Code 支持两种技能存放位置：

#### 1. 全局技能（所有项目可用）
```
~/.claude/skills/
├── process-faq/
│   ├── SKILL.md
│   ├── README.md
│   ├── requirements.txt
│   └── scripts/
├── playwright-skill/
│   ├── SKILL.md
│   ├── package.json
│   └── ...
└── d3-viz/
    ├── SKILL.md
    └── ...
```

#### 2. 项目特定技能（仅当前项目可用）
```
your-project/
├── .claude/
│   └── skills/
│       ├── process-faq/
│       ├── playwright-skill/
│       └── custom-skill/
└── src/
```

### 技能配置文件

每个技能必须包含一个 `SKILL.md` 文件，格式如下：

```markdown
---
name: skill-name
description: 技能的简短描述，说明何时使用此技能
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# 技能名称

技能的详细文档...
```

**YAML 前置元数据说明：**
- `name`: 技能的唯一标识符
- `description`: 简短描述，帮助 Claude 决定何时使用此技能
- `allowed-tools`: 该技能可以使用的 Claude Code 工具列表

### 使用技能

安装技能后，只需用自然语言描述你想做什么，Claude 会自动识别并使用合适的技能：

```
# 使用 process-faq 技能
"处理 FAQ.xlsx 并转换为 RAG 格式"

# 使用 playwright-skill 技能
"测试登录页面是否正常工作"

# 使用 d3-viz 技能
"用 D3.js 创建一个交互式柱状图"
```

### 技能优先级

当多个技能都可能适用时：
1. **项目特定技能**优先于全局技能
2. Claude 会根据 `description` 字段选择最匹配的技能
3. 你可以明确指定要使用的技能

### 调试技能

如果技能没有按预期工作：

1. **检查技能是否正确安装：**
   ```
   "列出所有可用的技能"
   ```

2. **查看技能文档：**
   ```
   "显示 process-faq 技能的文档"
   ```

3. **检查依赖是否安装：**
   ```bash
   # Python 技能
   pip list | grep -i pandas

   # Node.js 技能
   cd ~/.claude/skills/playwright-skill && npm list
   ```

4. **查看 Claude Code 日志：**
   - macOS: `~/Library/Logs/Claude Code/`
   - Linux: `~/.config/Claude Code/logs/`
   - Windows: `%APPDATA%\Claude Code\logs\`

### 环境变量配置

某些技能可能需要环境变量：

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export SKILL_SEEKER_API_KEY="your-api-key"
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.playwright"
```

### 最佳实践

1. **保持技能更新**：定期拉取最新版本
   ```bash
   cd claude-skills-suite && git pull
   ```

2. **使用项目特定技能**：为特定项目定制技能
3. **编写清晰的描述**：确保 `SKILL.md` 的 `description` 字段准确描述技能用途
4. **测试技能**：在实际使用前测试技能的所有功能
5. **备份配置**：在修改技能前备份原始配置

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
- `README.md` - 文档
- `requirements.txt` 或 `package.json` - 依赖（如需要）
- 支持脚本和文件

### 技能目录结构示例

```
my-custom-skill/
├── SKILL.md              # 必需：技能定义
├── README.md             # 推荐：详细文档
├── requirements.txt      # 如果是 Python 项目
├── package.json          # 如果是 Node.js 项目
├── scripts/              # 辅助脚本
│   ├── process.py
│   └── analyze.js
├── templates/            # 模板文件
│   └── output.template
└── tests/                # 测试文件
    └── test_skill.py
```

### SKILL.md 模板

```markdown
---
name: my-custom-skill
description: 简短描述技能的功能和使用场景。当用户请求 X 功能时使用此技能。
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# My Custom Skill

## 概述

技能的详细描述...

## 功能特性

- 特性 1
- 特性 2
- 特性 3

## 使用方法

### 基本用法

描述如何使用此技能...

### 高级用法

描述高级功能...

## 示例

提供实际使用示例...

## 依赖

列出所需的依赖...

## 故障排除

常见问题和解决方案...
```

### 技能开发指南

1. **明确的目标**：技能应该有一个清晰、具体的目标
2. **良好的文档**：详细说明技能的功能、使用方法和限制
3. **错误处理**：优雅地处理错误情况
4. **依赖管理**：清楚地列出所有依赖
5. **测试**：编写测试确保技能正常工作
6. **示例**：提供实际使用示例

---

## 贡献

欢迎贡献！添加新技能的步骤：

1. Fork 此仓库
2. 创建一个新的技能目录，包含适当的结构
3. 添加文档和示例
4. 提交 pull request

### 贡献指南

- 确保技能有清晰的 `SKILL.md` 和 `README.md`
- 提供使用示例
- 测试技能的所有功能
- 遵循现有技能的命名和结构约定
- 更新主 README.md 添加新技能的信息

---

## 技能路线图

计划中的技能：
- `analyze-code-quality` - 代码质量分析和建议
- `optimize-database` - 数据库架构优化
- `generate-tests` - 自动化测试生成
- `refactor-code` - 智能代码重构
- `security-audit` - 安全审计和漏洞检测
- `performance-profiling` - 性能分析和优化建议

---

## 支持

遇到问题或有疑问：
- 在 GitHub 上提交 issue
- 查看各个技能的文档
- 询问 Claude 寻求帮助

### 常见问题

**Q: 技能没有被 Claude 识别？**
A: 确保技能目录在 `~/.claude/skills/` 或项目的 `.claude/skills/` 中，并且包含有效的 `SKILL.md` 文件。

**Q: 如何更新技能？**
A: 运行 `git pull` 更新仓库，然后重新复制技能到 Claude 目录。

**Q: 可以同时使用多个技能吗？**
A: 可以，Claude 会根据任务需求自动选择和组合使用多个技能。

**Q: 如何禁用某个技能？**
A: 从 `~/.claude/skills/` 或 `.claude/skills/` 目录中移除该技能文件夹。

---

## 许可证

MIT License - 欢迎自由使用和修改这些技能。

---

## 关于

此技能套件由社区维护，旨在扩展 Claude Code 在常见开发任务中的能力。

**项目维护者**：jone_qian
**仓库地址**：https://github.com/jone_qian/claude-skills-suite
**贡献者**：欢迎所有贡献者

---

## 资源链接

- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Skill Seeker 详细文档](docs/)
- [示例配置文件](configs/)
- [问题追踪](https://github.com/jone_qian/claude-skills-suite/issues)

---

**祝你使用愉快！Happy Coding! 🚀**
