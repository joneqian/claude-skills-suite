# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Skills Suite is a collection of custom skills for Claude Code, combined with Skill Seeker - a tool for automatically generating Claude AI skills from documentation websites, GitHub repos, and PDFs.

## Repository Structure

```
claude-skills-suite/
├── skill_seekers/           # Main Python package
│   ├── cli/                 # CLI tools (doc_scraper, github_scraper, pdf_scraper, etc.)
│   └── mcp/                 # MCP server implementation (FastMCP-based)
├── configs/                 # Pre-built scraping configs for popular frameworks
├── output/                  # Generated skills and included skills
│   ├── process-faq/         # FAQ to RAG conversion skill
│   ├── playwright-skill/    # Browser automation testing
│   ├── d3js/                # D3.js visualization skill
│   └── product-manager-toolkit/  # PM tools (RICE, interview analysis)
└── *.sh                     # MCP server management scripts
```

## Commands

### MCP Server Management

```bash
# First-time setup (installs dependencies, configures MCP)
./skill_seeker_setup_mcp.sh

# Start HTTP server (default port 3000)
./skill_seeker_start_mcp.sh

# Start on custom port
./skill_seeker_start_mcp.sh -p 8080

# Run in foreground for debugging
./skill_seeker_start_mcp.sh -f

# Stop server
./skill_seeker_stop_mcp.sh
```

### CLI Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Scrape documentation
skill-seekers scrape --config configs/react.json

# Scrape GitHub repo
skill-seekers github --repo microsoft/TypeScript --name typescript

# Multi-source scraping
skill-seekers unified --config configs/react_unified.json

# Package skill for upload
skill-seekers package output/react/

# Install to Claude Code
skill-seekers install-agent output/react/ --agent claude

# Estimate pages before scraping
skill-seekers estimate configs/godot.json
```

### Python Development

```bash
# Install package in development mode
pip install -e .

# Run MCP server directly
python -m skill_seekers.mcp.server_fastmcp          # stdio mode
python -m skill_seekers.mcp.server_fastmcp --http   # HTTP mode
```

## Architecture

### Skill Seeker Components

1. **CLI Module** (`skill_seekers/cli/`): Command-line tools
   - `main.py` - Unified CLI entry point with git-style subcommands
   - `doc_scraper.py` - Website documentation scraper
   - `github_scraper.py` - GitHub repository scraper
   - `pdf_scraper.py` - PDF content extractor
   - `unified_scraper.py` - Multi-source combiner
   - `package_skill.py` - Skill packaging into .zip
   - `install_agent.py` - Install skills to AI agent directories

2. **MCP Module** (`skill_seekers/mcp/`): Model Context Protocol server
   - `server_fastmcp.py` - Main FastMCP server (17 tools across 5 categories)
   - `tools/` - Individual tool implementations
   - Supports both stdio and HTTP transports

3. **Config Files** (`configs/`): JSON configurations for scraping
   - Define base_url, start_urls, selectors, url_patterns, categories
   - Pre-built configs for React, Vue, Django, FastAPI, Kubernetes, etc.

### Included Skills (`output/`)

Each skill follows the Claude Code skill structure:
- `SKILL.md` - Required: YAML frontmatter (name, description, allowed-tools) + documentation
- Supporting scripts and dependencies

## Configuration Format

Scraping configs use this structure:
```json
{
  "name": "framework-name",
  "description": "When to use this skill",
  "base_url": "https://docs.example.com/",
  "start_urls": ["https://docs.example.com/getting-started"],
  "selectors": {
    "main_content": "article",
    "title": "h1"
  },
  "url_patterns": {
    "include": ["/docs", "/api"],
    "exclude": ["/blog"]
  },
  "max_pages": 100
}
```

## Key Dependencies

- Python 3.10+
- mcp, fastmcp - MCP protocol implementation
- requests, beautifulsoup4 - Web scraping
- uvicorn - HTTP server for MCP

## Server Files

When running HTTP mode, these files are created in project root:
- `.mcp-server.pid` - Process ID
- `.mcp-server.port` - Port number
- `.mcp-server.log` - Server logs
