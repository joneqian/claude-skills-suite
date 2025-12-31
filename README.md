# Claude Skills Suite

A collection of custom skills for Claude Code to extend its capabilities.

## Available Skills

### process-faq

Transform raw FAQ documents into RAG-optimized structured format.

**Features:**
- Analyze FAQ documents from multiple formats (Excel, Word, PDF, text)
- Identify structural and content quality issues
- Auto-generate categories and keywords
- Remove duplicates and merge similar questions
- Output standardized Excel format for RAG systems

**Use cases:**
- Knowledge base preparation
- Customer support FAQ organization
- RAG system data preparation
- FAQ quality improvement

[View Documentation →](process-faq/README.md)

## Installation

### For Claude Code

1. Clone this repository:
```bash
git clone https://github.com/jone_qian/claude-skills-suite.git
cd claude-skills-suite
```

2. Install dependencies for the skills you want to use:
```bash
# For process-faq
pip install -r process-faq/requirements.txt
```

3. Copy skills to Claude's skills directory:
```bash
# For personal use
cp -r process-faq ~/.claude/skills/

# For project-specific use
mkdir -p .claude/skills
cp -r process-faq .claude/skills/
```

4. Restart Claude Code

### Verify Installation

Start Claude Code and ask:
```
What skills are available?
```

You should see `process-faq` in the list.

## Usage

Once installed, simply describe what you want to do:

```
User: Process my FAQ.xlsx and convert it to RAG format

User: Analyze this customer support document and restructure it for RAG

User: I have a Word document with FAQs, can you help organize it?
```

Claude will automatically use the appropriate skill to help you.

## Skill Directory Structure

```
claude-skills-suite/
├── README.md
└── process-faq/
    ├── SKILL.md           # Skill definition
    ├── README.md          # Skill documentation
    ├── EXAMPLES.md        # Usage examples
    ├── requirements.txt   # Python dependencies
    └── scripts/
        ├── analyze_faq.py
        └── generate_rag_faq.py
```

## Creating Your Own Skills

Want to create a custom skill? See the [Claude Code Skills Documentation](https://github.com/anthropics/claude-code) for guidelines.

Each skill should have:
- `SKILL.md` - Skill definition with YAML frontmatter
- `README.md` - Documentation
- `requirements.txt` - Dependencies (if needed)
- Supporting scripts and files

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create a new skill directory with proper structure
3. Add documentation and examples
4. Submit a pull request

## Skills Roadmap

Planned skills:
- `analyze-code-quality` - Code quality analysis and recommendations
- `optimize-database` - Database schema optimization
- `generate-tests` - Automated test generation
- `refactor-code` - Intelligent code refactoring

## Support

For issues or questions:
- Open an issue on GitHub
- Check individual skill documentation
- Ask Claude for help

## License

MIT License - feel free to use and modify these skills for your needs.

## About

This skills suite is maintained by the community to extend Claude Code's capabilities for common development tasks.
