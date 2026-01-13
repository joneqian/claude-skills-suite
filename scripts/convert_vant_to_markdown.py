#!/usr/bin/env python3
"""
将 Vant 4 文档从 HTML 转换为 Markdown 格式

该脚本会：
1. 读取 output-scraped/vant 目录下的所有 HTML 文件
2. 提取每个页面的主体内容（去除导航、页眉、页脚等）
3. 转换为 Markdown 格式
4. 输出到 output/vant/references 目录，保持原有目录结构

Usage:
    python scripts/convert_vant_to_markdown.py
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, NavigableString


# 源目录和目标目录
SOURCE_DIR = Path(__file__).parent.parent / "output-scraped" / "vant"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "vant" / "references"


def clean_text(text: str) -> str:
    """清理文本，去除多余空白"""
    if not text:
        return ""
    # 去除多余的空白行和空格
    lines = [line.strip() for line in text.split("\n")]
    # 合并连续的空行
    result_lines = []
    prev_empty = False
    for line in lines:
        is_empty = not line
        if is_empty:
            if not prev_empty:
                result_lines.append("")
            prev_empty = True
        else:
            result_lines.append(line)
            prev_empty = False
    return "\n".join(result_lines).strip()


def html_to_markdown(element, level: int = 0) -> str:
    """将 HTML 元素递归转换为 Markdown"""
    if element is None:
        return ""

    if isinstance(element, NavigableString):
        text = str(element)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text)
        return text

    tag_name = element.name

    # 跳过的标签
    skip_tags = {"script", "style", "nav", "iframe", "img", "svg",
                 "van-doc-simulator", "button"}
    if tag_name in skip_tags:
        return ""

    # 跳过特定 class 的元素
    classes = element.get("class", [])
    skip_classes = ["van-doc-header", "van-doc-nav", "van-doc-simulator"]
    if any(skip_cls in " ".join(classes) for skip_cls in skip_classes):
        return ""

    # 处理标题
    if tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        heading_level = int(tag_name[1])
        text = element.get_text(strip=True)
        # 去除锚点链接符号
        text = text.replace("#", "").strip()
        if text:
            return f"\n{'#' * heading_level} {text}\n\n"
        return ""

    # 处理段落
    if tag_name == "p":
        content = "".join(html_to_markdown(child, level) for child in element.children)
        content = content.strip()
        if content:
            return f"\n{content}\n\n"
        return ""

    # 处理代码
    if tag_name == "code":
        text = element.get_text()
        if "\n" in text:
            # 多行代码
            lang = ""
            classes = element.get("class", [])
            for cls in classes:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
                    break
            return f"\n```{lang}\n{text.strip()}\n```\n"
        return f"`{text}`"

    # 处理 pre 标签（代码块）
    if tag_name == "pre":
        code_tag = element.find("code")
        if code_tag:
            class_list = code_tag.get("class", [])
        else:
            class_list = element.get("class", [])

        lang = ""
        for cls in class_list:
            if isinstance(cls, str) and cls.startswith("language-"):
                lang = cls.replace("language-", "")
                break

        if code_tag:
            content = code_tag.get_text()
        else:
            content = element.get_text()

        if lang:
            return f"\n```{lang}\n{content.strip()}\n```\n\n"
        return f"\n```\n{content.strip()}\n```\n\n"

    # 处理引用
    if tag_name == "blockquote":
        content = "".join(html_to_markdown(child, level) for child in element.children)
        content = content.strip()
        if content:
            lines = content.split("\n")
            quoted_lines = [f"> {line}" if line.strip() else ">" for line in lines]
            return "\n" + "\n".join(quoted_lines) + "\n\n"
        return ""

    # 处理链接
    if tag_name == "a":
        text = element.get_text(strip=True)
        href = element.get("href", "")
        if text and href:
            return f"[{text}]({href})"
        return text

    # 处理强调
    if tag_name in ("strong", "b"):
        text = element.get_text()
        return f"**{text}**"

    if tag_name in ("em", "i"):
        text = element.get_text()
        return f"*{text}*"

    # 处理列表
    if tag_name == "ul":
        items = []
        for li in element.find_all("li", recursive=False):
            content = "".join(html_to_markdown(child, level + 1) for child in li.children)
            content = content.strip()
            if content:
                items.append(f"- {content}")
        return "\n" + "\n".join(items) + "\n\n"

    if tag_name == "ol":
        items = []
        for i, li in enumerate(element.find_all("li", recursive=False), 1):
            content = "".join(html_to_markdown(child, level + 1) for child in li.children)
            content = content.strip()
            if content:
                items.append(f"{i}. {content}")
        return "\n" + "\n".join(items) + "\n\n"

    # 处理表格
    if tag_name == "table":
        return convert_table_to_markdown(element)

    # 处理 div 和 section
    if tag_name in ("div", "section", "article", "main"):
        content = "".join(html_to_markdown(child, level) for child in element.children)
        return content

    # 处理 span
    if tag_name == "span":
        return "".join(html_to_markdown(child, level) for child in element.children)

    # 处理 br
    if tag_name == "br":
        return "\n"

    # 处理 hr
    if tag_name == "hr":
        return "\n---\n\n"

    # 默认处理：递归处理子元素
    return "".join(html_to_markdown(child, level) for child in element.children)


def convert_table_to_markdown(table) -> str:
    """将 HTML 表格转换为 Markdown 表格"""
    rows = []

    # 处理表头
    thead = table.find("thead")
    if thead:
        header_row = thead.find("tr")
        if header_row:
            headers = []
            for th in header_row.find_all(["th", "td"]):
                headers.append(th.get_text(strip=True))
            if headers:
                rows.append("| " + " | ".join(headers) + " |")
                rows.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # 处理表体
    tbody = table.find("tbody")
    if tbody:
        for tr in tbody.find_all("tr"):
            cells = []
            for td in tr.find_all(["td", "th"]):
                # 处理单元格中的代码
                cell_content = []
                for child in td.children:
                    if hasattr(child, "name") and child.name == "code":
                        cell_content.append(f"`{child.get_text()}`")
                    elif isinstance(child, NavigableString):
                        cell_content.append(str(child).strip())
                    elif hasattr(child, "name") and child.name == "br":
                        cell_content.append("<br>")
                    elif hasattr(child, "name"):
                        cell_content.append(child.get_text(strip=True))

                cell_text = "".join(cell_content).replace("\n", " ").strip()
                # 转义管道符
                cell_text = cell_text.replace("|", "\\|")
                cells.append(cell_text)

            if cells:
                rows.append("| " + " | ".join(cells) + " |")

    if rows:
        return "\n" + "\n".join(rows) + "\n\n"
    return ""


def extract_main_content(html_content: str) -> str:
    """从 Vant HTML 中提取主体内容并转换为 Markdown"""
    soup = BeautifulSoup(html_content, "html.parser")

    # Vant 文档的主体内容区域
    doc_content = soup.find("div", class_="van-doc-content")
    if not doc_content:
        # 尝试查找其他可能的容器
        doc_content = soup.find("section", class_="van-doc-markdown-body")
        if not doc_content:
            doc_content = soup.find("body")
            if not doc_content:
                return ""

    # 移除不需要的元素
    for elem in doc_content.find_all(["van-doc-simulator", "script", "style"]):
        elem.decompose()

    # 提取标题
    title = ""
    title_elem = doc_content.find("h1")
    if title_elem:
        title = title_elem.get_text(strip=True)

    markdown_parts = []

    if title:
        markdown_parts.append(f"# {title}\n")

    # 查找 Markdown 内容区域
    markdown_body = doc_content.find("section", class_="van-doc-markdown-body")
    if markdown_body:
        content = html_to_markdown(markdown_body)
        markdown_parts.append(content)
    else:
        # 直接处理 doc_content
        content = html_to_markdown(doc_content)
        markdown_parts.append(content)

    # 合并并清理
    result = "\n".join(markdown_parts)
    result = clean_text(result)

    # 清理多余的空行
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result


def convert_file(source_path: Path, output_path: Path) -> bool:
    """转换单个文件"""
    try:
        # 读取 HTML
        with open(source_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 转换为 Markdown
        markdown_content = extract_main_content(html_content)

        if not markdown_content.strip():
            print(f"  警告: 未能提取内容 - {source_path}")
            return False

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入 Markdown 文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return True

    except Exception as e:
        print(f"  错误: {source_path} - {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("CONVERTING VANT HTML TO MARKDOWN")
    print("=" * 70)
    print()
    print(f"源目录: {SOURCE_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print()

    if not SOURCE_DIR.exists():
        print(f"错误: 源目录不存在 - {SOURCE_DIR}")
        print("请先运行 python scripts/scrape_vant.py 抓取文档")
        return

    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 查找所有 HTML 文件
    html_files = list(SOURCE_DIR.rglob("*.html"))
    print(f"找到 {len(html_files)} 个 HTML 文件")
    print()

    success_count = 0
    fail_count = 0

    for html_file in sorted(html_files):
        # 计算相对路径
        relative_path = html_file.relative_to(SOURCE_DIR)

        # 构建输出路径（将 .html 改为 .md）
        output_path = OUTPUT_DIR / relative_path.with_suffix(".md")

        print(f"转换: {relative_path}")

        if convert_file(html_file, output_path):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"📁 输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
