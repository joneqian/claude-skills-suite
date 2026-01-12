#!/usr/bin/env python3
"""
将 TDesign 小程序文档从 HTML 转换为 Markdown 格式

该脚本会：
1. 读取 output-scraped/tdesign-miniprogram 目录下的所有 HTML 文件
2. 提取每个页面的主体内容（去除导航、页眉、页脚等）
3. 转换为 Markdown 格式
4. 输出到 output/tdesign-miniprogram/references 目录，保持原有目录结构
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, NavigableString


# 源目录和目标目录
SOURCE_DIR = Path(__file__).parent.parent / "output-scraped" / "tdesign-miniprogram"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "tdesign-miniprogram" / "references"


def decode_pre_content(encoded_content: str) -> str:
    """解码 pre 标签中的 URL 编码内容"""
    try:
        return unquote(encoded_content)
    except Exception:
        return encoded_content


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


def extract_code_blocks(soup: BeautifulSoup) -> None:
    """处理代码块，解码 URL 编码的内容"""
    # 处理 td-code-block 中的 pre 标签
    for code_block in soup.find_all("td-code-block"):
        for pre_tag in code_block.find_all("pre"):
            slot_name = pre_tag.get("slot", "")
            lang = pre_tag.get("lang", "")
            
            # 获取并解码内容
            encoded_content = pre_tag.get_text()
            decoded_content = decode_pre_content(encoded_content)
            
            # 创建新的代码块格式
            if lang:
                code_text = f"\n```{lang}\n{decoded_content}\n```\n"
            else:
                code_text = f"\n```\n{decoded_content}\n```\n"
            
            pre_tag.replace_with(code_text)
    
    # 处理普通的 pre 和 code 标签
    for pre_tag in soup.find_all("pre", class_=lambda x: x and "language-" in str(x)):
        class_list = pre_tag.get("class", [])
        lang = ""
        for cls in class_list:
            if cls.startswith("language-"):
                lang = cls.replace("language-", "")
                break
        
        code_tag = pre_tag.find("code")
        if code_tag:
            code_content = code_tag.get_text()
        else:
            code_content = pre_tag.get_text()
        
        if lang:
            new_content = f"\n```{lang}\n{code_content.strip()}\n```\n"
        else:
            new_content = f"\n```\n{code_content.strip()}\n```\n"
        
        pre_tag.replace_with(new_content)


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
    skip_tags = {"script", "style", "nav", "td-doc-phone", "td-contributors", 
                 "td-doc-footer", "td-doc-history", "td-theme-generator", "td-portal",
                 "iframe", "img"}
    if tag_name in skip_tags:
        return ""
    
    # 处理标题
    if tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        heading_level = int(tag_name[1])
        text = element.get_text(strip=True)
        # 去除锚点链接符号
        text = text.replace(" ", "").strip()
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
            return f"\n```\n{text.strip()}\n```\n"
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
    
    # 处理 div
    if tag_name == "div":
        content = "".join(html_to_markdown(child, level) for child in element.children)
        return content
    
    # 处理 td-code-block（代码示例块）
    if tag_name == "td-code-block":
        result = []
        for pre_tag in element.find_all("pre"):
            slot_name = pre_tag.get("slot", "")
            lang = pre_tag.get("lang", "")
            
            # 解码内容
            encoded_content = pre_tag.get_text()
            decoded_content = decode_pre_content(encoded_content)
            
            if slot_name and lang:
                result.append(f"\n**{slot_name}** (`{lang}`):\n```{lang}\n{decoded_content}\n```\n")
            elif lang:
                result.append(f"\n```{lang}\n{decoded_content}\n```\n")
            else:
                result.append(f"\n```\n{decoded_content}\n```\n")
        
        return "\n".join(result) + "\n"
    
    # 处理 span 和其他内联元素
    if tag_name in ("span", "td-doc-tabs"):
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
    """从 HTML 中提取主体内容并转换为 Markdown"""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 查找主体内容区域
    doc_content = soup.find("td-doc-content")
    if not doc_content:
        # 如果没有找到，尝试整个 body
        doc_content = soup.find("body")
        if not doc_content:
            return ""
    
    # 提取标题
    title = ""
    title_elem = doc_content.find("h1", id="__td_doc_title__")
    if title_elem:
        title = title_elem.get_text(strip=True)
    
    # 查找文档内容
    markdown_parts = []
    
    if title:
        markdown_parts.append(f"# {title}\n")
    
    # 查找 DOC 区域（普通文档页面）
    doc_div = doc_content.find("div", attrs={"name": "DOC"})
    if doc_div:
        # 跳过目录导航
        for toc in doc_div.find_all("nav", class_="tdesign-toc_container"):
            toc.decompose()
        
        content = html_to_markdown(doc_div)
        markdown_parts.append(content)
    
    # 查找 td-doc-main（组件页面）
    main_div = doc_content.find("div", class_="td-doc-main")
    if main_div:
        # 处理 DEMO 部分
        demo_div = main_div.find("div", attrs={"name": "DEMO"})
        if demo_div:
            # 跳过目录导航
            for toc in demo_div.find_all("nav", class_="tdesign-toc_container"):
                toc.decompose()
            
            markdown_parts.append("\n## 示例\n")
            content = html_to_markdown(demo_div)
            markdown_parts.append(content)
    
    # 处理 API 部分（可能在 td-doc-main 外面，直接在 td-doc-content 下）
    api_div = doc_content.find("div", attrs={"name": "API"})
    if api_div:
        # 跳过目录导航
        for toc in api_div.find_all("nav", class_="tdesign-toc_container"):
            toc.decompose()
        
        markdown_parts.append("\n## API\n")
        content = html_to_markdown(api_div)
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
    print(f"源目录: {SOURCE_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print()
    
    if not SOURCE_DIR.exists():
        print(f"错误: 源目录不存在 - {SOURCE_DIR}")
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
    print(f"转换完成: 成功 {success_count}, 失败 {fail_count}")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
