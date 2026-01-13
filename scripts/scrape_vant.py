#!/usr/bin/env python3
"""
Scrape Vant 4 documentation using Playwright for JS-rendered content.
Outputs organized HTML files based on URL structure.

Usage:
    python scripts/scrape_vant.py
"""

import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

# Configuration
CONFIG_FILE = Path(__file__).parent.parent / "configs" / "vant.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output-scraped" / "vant"
RATE_LIMIT = 0.5  # seconds between requests


def load_config() -> dict:
    """Load configuration from JSON file."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_url_to_path(url: str) -> tuple[Path, str]:
    """
    Parse Vant URL to determine output path and filename.

    Vant uses hash routing: #/zh-CN/button

    Returns:
        tuple: (directory_path, filename)

    Examples:
        - https://vant-ui.github.io/vant/#/zh-CN/home
          → zh-CN/home.html
        - https://vant-ui.github.io/vant/#/zh-CN/button
          → zh-CN/components/button.html
        - https://vant-ui.github.io/vant/#/zh-CN/use-click-away
          → zh-CN/composables/use-click-away.html
    """
    # Extract hash path: #/zh-CN/button → /zh-CN/button
    if "#" in url:
        hash_part = url.split("#")[1]
    else:
        hash_part = "/zh-CN/home"

    # Remove leading slash
    path = hash_part.strip("/")
    parts = path.split("/")

    if len(parts) < 2:
        return Path("zh-CN"), "index.html"

    lang = parts[0]  # zh-CN or en-US
    page = parts[1] if len(parts) > 1 else "index"

    # Categorize pages
    getting_started = ["home", "quickstart", "advanced-usage", "faq", "locale"]
    composables = [
        "vant-use-intro", "use-click-away", "use-count-down",
        "use-custom-field-value", "use-event-listener", "use-page-visibility",
        "use-rect", "use-relation", "use-scroll-parent", "use-toggle",
        "use-window-size", "use-raf"
    ]

    if page in getting_started:
        dir_path = Path(lang) / "getting-started"
    elif page in composables or page.startswith("use-"):
        dir_path = Path(lang) / "composables"
    else:
        dir_path = Path(lang) / "components"

    filename = f"{page}.html"

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
    print("SCRAPING VANT 4 DOCUMENTATION")
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

    getting_started = [r for r in results["success"]
                       if "getting-started" in r["path"]]
    components = [r for r in results["success"]
                  if "components" in r["path"]]
    composables = [r for r in results["success"]
                   if "composables" in r["path"]]

    print(f"  zh-CN/getting-started/: {len(getting_started)} files")
    print(f"  zh-CN/components/: {len(components)} files")
    print(f"  zh-CN/composables/: {len(composables)} files")

    return results


if __name__ == "__main__":
    asyncio.run(main())
