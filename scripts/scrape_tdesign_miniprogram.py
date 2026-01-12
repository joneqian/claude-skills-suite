#!/usr/bin/env python3
"""
Scrape TDesign Mini Program documentation using Playwright for JS-rendered content.
Outputs organized HTML files based on URL structure.
"""

import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from playwright.async_api import async_playwright

# Configuration
CONFIG_FILE = Path(__file__).parent.parent / \
    "configs" / "tdesign-miniprogram.json"
OUTPUT_DIR = Path(__file__).parent.parent / \
    "output-scraped" / "tdesign-miniprogram"
RATE_LIMIT = 1.0  # seconds between requests


def load_config() -> dict:
    """Load configuration from JSON file."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_url_to_path(url: str) -> tuple[Path, str]:
    """
    Parse URL to determine output path and filename.

    Returns:
        tuple: (directory_path, filename)

    Examples:
        - https://tdesign.tencent.com/miniprogram/getting-started 
          → miniprogram/getting-started/index.html
        - https://tdesign.tencent.com/miniprogram/components/button?tab=demo 
          → miniprogram/components/button/demo.html
        - https://tdesign.tencent.com/miniprogram-chat/components/chat-list?tab=api 
          → miniprogram-chat/components/chat-list/api.html
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    query_params = parse_qs(parsed.query)

    # Determine the base directory (miniprogram or miniprogram-chat)
    if "miniprogram-chat" in path_parts:
        base_dir = "miniprogram-chat"
        # Remove 'miniprogram-chat' from path parts
        idx = path_parts.index("miniprogram-chat")
        remaining_parts = path_parts[idx + 1:]
    elif "miniprogram" in path_parts:
        base_dir = "miniprogram"
        # Remove 'miniprogram' from path parts
        idx = path_parts.index("miniprogram")
        remaining_parts = path_parts[idx + 1:]
    else:
        # Fallback
        base_dir = "other"
        remaining_parts = path_parts

    # Build directory path
    if not remaining_parts:
        dir_path = Path(base_dir)
        filename = "index.html"
    elif "components" in remaining_parts:
        # Component URL: miniprogram/components/button?tab=demo
        comp_idx = remaining_parts.index("components")
        if comp_idx + 1 < len(remaining_parts):
            component_name = remaining_parts[comp_idx + 1]
            dir_path = Path(base_dir) / "components" / component_name

            # Determine filename based on tab parameter
            tab = query_params.get("tab", ["index"])[0]
            filename = f"{tab}.html"
        else:
            dir_path = Path(base_dir) / "components"
            filename = "index.html"
    else:
        # Non-component URL: miniprogram/getting-started
        page_name = remaining_parts[-1] if remaining_parts else "index"
        if len(remaining_parts) > 1:
            dir_path = Path(base_dir) / \
                "/".join(remaining_parts[:-1]) / page_name
        else:
            dir_path = Path(base_dir) / page_name
        filename = "index.html"

    return dir_path, filename


async def scrape_page(page, url: str) -> dict | None:
    """Scrape a single page and return its full HTML content."""
    try:
        print(f"  → Loading: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2000)  # Extra wait for dynamic content

        # Get page title
        title = await page.title()

        # Get the full rendered page HTML
        html_content = await page.content()

        return {
            "url": url,
            "title": title,
            "html": html_content,
            "html_length": len(html_content),
        }

    except Exception as e:
        print(f"  ✗ Error scraping {url}: {e}")
        return None


def save_html_file(html_content: str, output_path: Path) -> None:
    """Save the full HTML content to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


async def main():
    """Main scraping function."""
    print("=" * 70)
    print("SCRAPING TDESIGN MINIPROGRAM DOCUMENTATION")
    print("=" * 70)
    print()

    # Load configuration
    config = load_config()
    start_urls = config.get("start_urls", [])

    print(f"📋 Found {len(start_urls)} URLs to scrape")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Track results
    results = {
        "success": [],
        "failed": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )
        page = await context.new_page()

        for idx, url in enumerate(start_urls, 1):
            print(f"\n[{idx}/{len(start_urls)}] Processing: {url}")

            # Parse URL to get output path
            dir_path, filename = parse_url_to_path(url)
            output_path = OUTPUT_DIR / dir_path / filename

            print(f"  → Output: {dir_path}/{filename}")

            # Scrape the page
            data = await scrape_page(page, url)

            if data:
                # Save full HTML file
                save_html_file(data["html"], output_path)
                results["success"].append({
                    "url": url,
                    "path": str(dir_path / filename),
                    "title": data["title"],
                    "html_length": data["html_length"],
                })
                print(
                    f"  ✓ Saved: {data['title'][:50]}... ({data['html_length']} chars)")
            else:
                results["failed"].append(url)
                print(f"  ✗ Failed to scrape")

            # Rate limiting
            await asyncio.sleep(RATE_LIMIT)

        await browser.close()

    # Save summary
    summary_file = OUTPUT_DIR / "scrape_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print summary
    print()
    print("=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"✅ Success: {len(results['success'])} pages")
    print(f"❌ Failed: {len(results['failed'])} pages")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"📋 Summary: {summary_file}")

    if results["failed"]:
        print("\nFailed URLs:")
        for url in results["failed"]:
            print(f"  - {url}")

    # Print directory structure summary
    print("\nDirectory Structure:")

    miniprogram_pages = [r for r in results["success"]
                         if r["path"].startswith("miniprogram/")]
    chat_pages = [r for r in results["success"]
                  if r["path"].startswith("miniprogram-chat/")]

    print(f"  miniprogram/: {len(miniprogram_pages)} files")
    print(f"  miniprogram-chat/: {len(chat_pages)} files")

    return results


if __name__ == "__main__":
    asyncio.run(main())
