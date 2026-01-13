#!/usr/bin/env python3
"""
Playwright-based scraper for SPA (Single Page Application) websites.

This module provides a reusable PlaywrightScraper class that can render
JavaScript-heavy pages and extract content that would otherwise be
inaccessible via traditional HTTP requests.

Usage:
    from playwright_scraper import PlaywrightScraper

    scraper = PlaywrightScraper(config)
    results = await scraper.scrape_all(urls)
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PlaywrightScraper:
    """
    Reusable Playwright scraper for SPA websites.

    Supports:
    - JavaScript rendering via headless Chromium
    - Configurable wait strategies (networkidle, load, domcontentloaded)
    - Rate limiting between requests
    - Retry mechanism with exponential backoff
    - Progress logging
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Playwright scraper.

        Args:
            config: Configuration dictionary with optional keys:
                - rate_limit: Seconds between requests (default: 0.5)
                - playwright_config: Dict with Playwright-specific settings:
                    - wait_until: "networkidle" | "load" | "domcontentloaded"
                    - timeout: Page load timeout in ms (default: 60000)
                    - extra_wait: Additional wait after load in ms (default: 2000)
                    - headless: Run browser headless (default: True)
                    - max_retries: Max retry attempts (default: 3)
        """
        self.config = config
        self.rate_limit = config.get('rate_limit', 0.5)

        # Playwright-specific config
        pw_config = config.get('playwright_config', {})
        self.wait_until = pw_config.get('wait_until', 'networkidle')
        self.timeout = pw_config.get('timeout', 60000)
        self.extra_wait = pw_config.get('extra_wait', 2000)
        self.headless = pw_config.get('headless', True)
        self.max_retries = pw_config.get('max_retries', 3)

    async def scrape_page(
        self,
        page: Any,
        url: str
    ) -> Optional[Dict[str, Any]]:
        """
        Scrape a single page with retry support.

        Args:
            page: Playwright Page object
            url: URL to scrape

        Returns:
            Dict with {url, title, html, html_length} or None on failure
        """
        for attempt in range(self.max_retries):
            try:
                logger.info("  %s", url)

                await page.goto(
                    url,
                    wait_until=self.wait_until,
                    timeout=self.timeout
                )

                # Extra wait for dynamic content (crucial for SPAs)
                await page.wait_for_timeout(self.extra_wait)

                title = await page.title()
                html = await page.content()

                return {
                    "url": url,
                    "title": title,
                    "html": html,
                    "html_length": len(html),
                }

            except Exception as e:
                error_type = type(e).__name__
                logger.warning(
                    "  ⚠ Attempt %d/%d failed for %s: %s",
                    attempt + 1, self.max_retries, url, error_type
                )

                if attempt < self.max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)

                    # Reload on timeout errors
                    if "Timeout" in error_type:
                        try:
                            await page.reload()
                        except Exception:
                            pass
                else:
                    logger.error("  ✗ Failed: %s", url)

        return None

    async def scrape_all(
        self,
        urls: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Scrape all URLs using Playwright.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of successfully scraped page data
        """
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error(
                "❌ Playwright not installed. Install with:\n"
                "   pip install playwright\n"
                "   playwright install chromium"
            )
            raise ImportError(
                "Playwright is required for SPA scraping. "
                "Install with: pip install playwright && playwright install chromium"
            )

        results: List[Dict[str, Any]] = []
        failed: List[str] = []

        logger.info("\n🎭 Starting Playwright scraper (SPA mode)")
        logger.info("   URLs to scrape: %d", len(urls))
        logger.info("   Wait strategy: %s", self.wait_until)
        logger.info("   Rate limit: %.1fs\n", self.rate_limit)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
            )
            page = await context.new_page()

            for idx, url in enumerate(urls, 1):
                logger.info("[%d/%d] Scraping...", idx, len(urls))

                result = await self.scrape_page(page, url)

                if result:
                    results.append(result)
                else:
                    failed.append(url)

                # Rate limiting
                if idx < len(urls):
                    await asyncio.sleep(self.rate_limit)

            await browser.close()

        logger.info("\n✅ Playwright scraping complete")
        logger.info("   Success: %d", len(results))
        logger.info("   Failed: %d", len(failed))

        if failed:
            logger.warning("\n   Failed URLs:")
            for url in failed[:10]:  # Show first 10
                logger.warning("   - %s", url)
            if len(failed) > 10:
                logger.warning("   ... and %d more", len(failed) - 10)

        return results


async def main():
    """Test the scraper with a sample config."""
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    # Test with a simple URL
    config = {
        "rate_limit": 1.0,
        "playwright_config": {
            "wait_until": "networkidle",
            "timeout": 60000,
            "extra_wait": 2000,
        }
    }

    test_urls = [
        "https://vant-ui.github.io/vant/#/zh-CN/button",
    ]

    scraper = PlaywrightScraper(config)
    results = await scraper.scrape_all(test_urls)

    for r in results:
        print(f"\n📄 {r['title']}")
        print(f"   URL: {r['url']}")
        print(f"   HTML length: {r['html_length']} chars")


if __name__ == "__main__":
    asyncio.run(main())
