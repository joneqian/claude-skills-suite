#!/usr/bin/env python3
"""
Build WeChat Mini Program skill from scraped data.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# Paths
SCRAPED_FILE = Path(__file__).parent.parent / "output" / "wechat-miniprogram" / "scraped" / "pages.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "wechat-miniprogram"
REFERENCES_DIR = OUTPUT_DIR / "references"


def load_scraped_data():
    """Load scraped pages data."""
    with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_code_examples(pages, max_examples=10):
    """Extract code examples from pages."""
    examples = []
    seen_codes = set()

    for page in pages:
        for block in page.get("code_blocks", []):
            code = block.get("code", "").strip()
            lang = block.get("language", "text")

            # Skip if too short, too long, or duplicate
            if len(code) < 20 or len(code) > 500:
                continue
            if code in seen_codes:
                continue

            # Prefer certain languages
            if lang in ["javascript", "js", "json", "wxml", "wxss", "html", "css"]:
                seen_codes.add(code)
                examples.append({
                    "language": lang,
                    "code": code,
                    "source": page.get("title", "Unknown")
                })

            if len(examples) >= max_examples:
                break

        if len(examples) >= max_examples:
            break

    return examples


def create_reference_file(category: str, pages: list) -> str:
    """Create a reference markdown file for a category."""
    content = f"# {category.replace('_', ' ').title()}\n\n"
    content += f"*{len(pages)} pages in this category*\n\n"
    content += "## Table of Contents\n\n"

    for i, page in enumerate(pages[:50], 1):  # Limit to 50 pages per category
        title = page.get("title", "Untitled").split(" | ")[0].strip()
        content += f"{i}. [{title}](#{i}-{title.lower().replace(' ', '-')[:30]})\n"

    content += "\n---\n\n"

    for i, page in enumerate(pages[:50], 1):
        title = page.get("title", "Untitled").split(" | ")[0].strip()
        url = page.get("url", "")
        page_content = page.get("content", "")

        content += f"## {i}. {title}\n\n"
        content += f"**Source**: [{url}]({url})\n\n"

        # Truncate content if too long
        if len(page_content) > 3000:
            page_content = page_content[:3000] + "\n\n... (content truncated)"

        content += page_content + "\n\n"

        # Add code examples
        for block in page.get("code_blocks", [])[:3]:
            lang = block.get("language", "text")
            code = block.get("code", "")
            if code and len(code) < 1000:
                content += f"```{lang}\n{code}\n```\n\n"

        content += "---\n\n"

    return content


def create_skill_md(pages: list, examples: list) -> str:
    """Create the main SKILL.md file."""
    content = """---
name: wechat-miniprogram
description: WeChat Mini Program development framework. Use for building WeChat mini apps, WXML templates, WXSS styles, WXS scripting, component development, and WeChat API integration.
---

# WeChat Mini Program Skill

WeChat Mini Program (微信小程序) development framework skill, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

- Developing WeChat Mini Programs (微信小程序)
- Working with WXML, WXSS, or WXS
- Using WeChat Mini Program APIs
- Building WeChat components
- Implementing WeChat open capabilities (开放能力)
- Debugging Mini Program issues
- Optimizing Mini Program performance

## Quick Reference

### Project Structure

```
├── app.js          # App logic
├── app.json        # App configuration
├── app.wxss        # Global styles
├── pages/
│   └── index/
│       ├── index.js    # Page logic
│       ├── index.json  # Page configuration
│       ├── index.wxml  # Page template
│       └── index.wxss  # Page styles
└── components/     # Custom components
```

### Common Patterns

"""

    # Add code examples
    for i, example in enumerate(examples, 1):
        lang = example.get("language", "text")
        code = example.get("code", "")
        source = example.get("source", "")

        content += f"**Example {i}** ({lang}):\n\n"
        content += f"```{lang}\n{code}\n```\n\n"

    content += """
## Reference Files

This skill includes comprehensive documentation in `references/`:

- **getting_started.md** - Quick start and introduction
- **framework.md** - Mini Program framework (逻辑层、视图层)
- **components.md** - Built-in components
- **api.md** - API reference
- **cloud.md** - Cloud development (云开发)
- **reference.md** - Configuration reference

Use `view` to read specific reference files when detailed information is needed.

## Key Concepts

### App Lifecycle

```javascript
App({
  onLaunch(options) {
    // Mini Program initialized
  },
  onShow(options) {
    // Mini Program shown
  },
  onHide() {
    // Mini Program hidden
  },
  globalData: {
    userInfo: null
  }
})
```

### Page Lifecycle

```javascript
Page({
  data: {
    message: 'Hello World'
  },
  onLoad(options) {
    // Page loaded
  },
  onShow() {
    // Page shown
  },
  onReady() {
    // Page ready
  },
  onHide() {
    // Page hidden
  },
  onUnload() {
    // Page unloaded
  }
})
```

### WXML Data Binding

```wxml
<view>{{message}}</view>
<view wx:if="{{condition}}">Conditional</view>
<view wx:for="{{array}}" wx:key="id">{{item}}</view>
```

### Event Handling

```wxml
<button bindtap="handleTap">Click Me</button>
```

```javascript
Page({
  handleTap(e) {
    console.log(e)
  }
})
```

## Working with This Skill

### For Beginners
Start with the getting_started reference file for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, framework, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

- [Official Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [Component Library](https://developers.weixin.qq.com/miniprogram/dev/component/)
- [API Reference](https://developers.weixin.qq.com/miniprogram/dev/api/)

## Notes

- This skill was automatically generated from official WeChat documentation
- Reference files preserve the structure and examples from source docs
- Content is in Chinese as per official documentation
"""

    return content


def main():
    print("=" * 60)
    print("BUILDING WECHAT MINIPROGRAM SKILL")
    print("=" * 60)
    print()

    # Load data
    print("Loading scraped data...")
    pages = load_scraped_data()
    print(f"  ✓ Loaded {len(pages)} pages")

    # Group by category
    print("\nGrouping by category...")
    categories = defaultdict(list)
    for page in pages:
        cat = page.get("category", "other")
        categories[cat].append(page)

    for cat, cat_pages in categories.items():
        print(f"  - {cat}: {len(cat_pages)} pages")

    # Create references directory
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    # Create reference files
    print("\nCreating reference files...")
    for cat, cat_pages in categories.items():
        ref_content = create_reference_file(cat, cat_pages)
        ref_file = REFERENCES_DIR / f"{cat}.md"
        with open(ref_file, "w", encoding="utf-8") as f:
            f.write(ref_content)
        print(f"  ✓ {cat}.md ({len(cat_pages)} pages)")

    # Extract code examples
    print("\nExtracting code examples...")
    examples = extract_code_examples(pages)
    print(f"  ✓ Extracted {len(examples)} examples")

    # Create SKILL.md
    print("\nCreating SKILL.md...")
    skill_content = create_skill_md(pages, examples)
    skill_file = OUTPUT_DIR / "SKILL.md"
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(skill_content)
    print(f"  ✓ SKILL.md created")

    # Create index
    print("\nCreating index.md...")
    index_content = "# WeChat Mini Program Skill\n\n"
    index_content += "## Reference Files\n\n"
    for cat in sorted(categories.keys()):
        index_content += f"- [{cat.replace('_', ' ').title()}](references/{cat}.md)\n"

    index_file = OUTPUT_DIR / "index.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"  ✓ index.md created")

    print()
    print("=" * 60)
    print(f"✅ Skill built: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
