#!/usr/bin/env python3
"""
Scrape WeChat Mini Program documentation using Playwright for JS-rendered content.
"""

import asyncio
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

# Configuration
BASE_URL = "https://developers.weixin.qq.com"
START_URLS = [
    "https://developers.weixin.qq.com/miniprogram/dev/framework/",
    "https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/",
    "https://developers.weixin.qq.com/miniprogram/dev/component/",
    "https://developers.weixin.qq.com/miniprogram/dev/api/",
    "https://developers.weixin.qq.com/miniprogram/dev/reference/",
]

URL_PATTERNS = {
    "include": ["/miniprogram/dev/"],
    "exclude": ["/community/", "/blog/", "/news/", "/qa/", "#"],
}

MAX_PAGES = 200
RATE_LIMIT = 1.0  # seconds between requests
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "wechat-miniprogram" / "scraped"

# Categories for organizing content
CATEGORIES = {
    "getting_started": ["quickstart", "intro", "getstart", "小程序介绍", "起步"],
    "framework": ["framework", "app", "page", "runtime", "运行时", "逻辑层", "视图层"],
    "view": ["wxml", "wxss", "wxs", "view", "template"],
    "components": ["component", "组件"],
    "api": ["api", "接口"],
    "tools": ["devtools", "tool", "工具"],
    "cloud": ["cloud", "云开发"],
    "reference": ["reference", "配置", "configuration"],
}


def should_include_url(url: str) -> bool:
    """Check if URL should be included based on patterns."""
    parsed = urlparse(url)
    path = parsed.path

    # Check exclude patterns first
    for pattern in URL_PATTERNS["exclude"]:
        if pattern in url:
            return False

    # Check include patterns
    for pattern in URL_PATTERNS["include"]:
        if pattern in path:
            return True

    return False


def categorize_page(url: str, title: str) -> str:
    """Categorize a page based on URL and title."""
    combined = f"{url} {title}".lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in combined:
                return category

    return "other"


async def scrape_page(page, url: str) -> dict | None:
    """Scrape a single page."""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)  # Extra wait for dynamic content

        # Get page title
        title = await page.title()

        # Try multiple selectors for main content
        content_selectors = [
            ".markdown-section",
            ".content-area",
            "article",
            ".doc-content",
            ".main-content",
            "main",
        ]

        content = ""
        for selector in content_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    content = await element.inner_text()
                    if len(content) > 100:  # Valid content found
                        break
            except Exception:
                continue

        if not content or len(content) < 50:
            print(f"  ⚠ No content: {url}")
            return None

        # Get code blocks
        code_blocks = []
        code_elements = await page.query_selector_all("pre code")
        for code_el in code_elements:
            try:
                code_text = await code_el.inner_text()
                code_class = await code_el.get_attribute("class") or ""
                lang_match = re.search(r"language-(\w+)", code_class)
                lang = lang_match.group(1) if lang_match else "text"
                code_blocks.append({"language": lang, "code": code_text})
            except Exception:
                continue

        # Find links for crawling
        links = []
        link_elements = await page.query_selector_all("a[href]")
        for link_el in link_elements:
            try:
                href = await link_el.get_attribute("href")
                if href:
                    full_url = urljoin(url, href)
                    if should_include_url(full_url) and full_url.startswith(BASE_URL):
                        links.append(full_url)
            except Exception:
                continue

        return {
            "url": url,
            "title": title,
            "content": content,
            "code_blocks": code_blocks,
            "links": list(set(links)),
            "category": categorize_page(url, title),
        }

    except Exception as e:
        print(f"  ✗ Error scraping {url}: {e}")
        return None


async def main():
    """Main scraping function."""
    print("=" * 60)
    print("SCRAPING WECHAT MINIPROGRAM DOCUMENTATION")
    print("=" * 60)
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    visited = set()
    to_visit = list(START_URLS)
    scraped_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        while to_visit and len(scraped_data) < MAX_PAGES:
            url = to_visit.pop(0)

            if url in visited:
                continue

            visited.add(url)
            print(f"[{len(scraped_data) + 1}/{MAX_PAGES}] Scraping: {url}")

            data = await scrape_page(page, url)

            if data:
                scraped_data.append(data)

                # Add new links to queue
                for link in data.get("links", []):
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)

                print(f"  ✓ {data['title'][:50]}... ({len(data['content'])} chars)")

            # Rate limiting
            await asyncio.sleep(RATE_LIMIT)

        await browser.close()

    # Save scraped data
    output_file = OUTPUT_DIR / "pages.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print(f"✅ Scraped {len(scraped_data)} pages")
    print(f"📁 Saved to: {output_file}")
    print("=" * 60)

    # Print category summary
    categories = {}
    for item in scraped_data:
        cat = item.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count} pages")

    return scraped_data


if __name__ == "__main__":
    asyncio.run(main())
