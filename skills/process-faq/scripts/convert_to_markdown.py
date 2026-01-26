#!/usr/bin/env python3
"""
Convert documents to Markdown format for Claude to analyze
Simply extracts and presents the raw content without interpretation.
Supports: Excel (.xlsx), Word (.docx), PDF (.pdf), Text (.txt)
"""

import sys
from pathlib import Path
from typing import List
import pandas as pd

# Import document readers
try:
    import openpyxl
    from docx import Document
    import PyPDF2
except ImportError as e:
    print(f"Error: Missing required library. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


class DocumentToMarkdown:
    """Convert various document formats to Markdown - raw content only."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = None

    def load_document(self) -> bool:
        """Load document based on file extension."""
        if not self.file_path.exists():
            print(f"Error: File not found: {self.file_path}")
            return False

        ext = self.file_path.suffix.lower()

        try:
            if ext == '.xlsx':
                self.content = self._load_excel()
            elif ext == '.docx':
                self.content = self._load_word()
            elif ext == '.pdf':
                self.content = self._load_pdf()
            elif ext in ['.txt', '.md']:
                self.content = self._load_text()
            else:
                print(f"Error: Unsupported file format: {ext}")
                return False
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def _load_excel(self) -> pd.DataFrame:
        """Load Excel file and return as DataFrame."""
        return pd.read_excel(self.file_path)

    def _load_word(self) -> List[str]:
        """Load Word document and return paragraphs."""
        doc = Document(self.file_path)
        return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    def _load_pdf(self) -> List[str]:
        """Load PDF file and return text content."""
        text_content = []
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append({
                        'page': page_num,
                        'text': text.strip()
                    })
        return text_content

    def _load_text(self) -> str:
        """Load text file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def convert_to_markdown(self) -> str:
        """Convert loaded content to Markdown format - raw presentation."""
        if isinstance(self.content, pd.DataFrame):
            return self._convert_dataframe_to_markdown()
        elif isinstance(self.content, list):
            if self.file_path.suffix.lower() == '.pdf':
                return self._convert_pdf_to_markdown()
            else:
                return self._convert_word_to_markdown()
        else:
            return self._convert_text_to_markdown()

    def _convert_dataframe_to_markdown(self) -> str:
        """Convert DataFrame to Markdown - show as-is table."""
        df = self.content

        markdown_lines = [
            f"# 文档内容: {self.file_path.name}",
            f"",
            f"**文件类型**: Excel (.xlsx)",
            f"**行数**: {len(df)}",
            f"**列数**: {len(df.columns)}",
            f"",
            f"---",
            f"",
            f"## 原始数据表格",
            f""
        ]

        # Convert DataFrame to Markdown table
        # Add header
        header = "| " + " | ".join(str(col) for col in df.columns) + " |"
        separator = "|" + "|".join([" --- " for _ in df.columns]) + "|"

        markdown_lines.append(header)
        markdown_lines.append(separator)

        # Add rows
        for _, row in df.iterrows():
            row_values = []
            for val in row:
                # Handle different types
                if pd.isna(val):
                    row_values.append("[空白]")
                else:
                    # Escape pipe characters in cell content
                    cell_value = str(val).replace("|", "\\|").replace("\n", " ")
                    row_values.append(cell_value)

            row_line = "| " + " | ".join(row_values) + " |"
            markdown_lines.append(row_line)

        # Add summary statistics
        markdown_lines.append("")
        markdown_lines.append("---")
        markdown_lines.append("")
        markdown_lines.append("## 数据统计")
        markdown_lines.append("")

        # Check for empty cells
        for col in df.columns:
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                markdown_lines.append(f"- **{col}**: {empty_count} 个空值")

        # Show data types
        markdown_lines.append("")
        markdown_lines.append("## 列信息")
        markdown_lines.append("")
        for col in df.columns:
            non_empty = df[col].dropna()
            if len(non_empty) > 0:
                sample = str(non_empty.iloc[0])[:50]
                markdown_lines.append(f"- **{col}**: 示例数据 = \"{sample}...\"")
            else:
                markdown_lines.append(f"- **{col}**: [全部为空]")

        return "\n".join(markdown_lines)

    def _convert_word_to_markdown(self) -> str:
        """Convert Word paragraphs to Markdown - raw paragraphs."""
        markdown_lines = [
            f"# 文档内容: {self.file_path.name}",
            f"",
            f"**文件类型**: Word (.docx)",
            f"**段落数**: {len(self.content)}",
            f"",
            f"---",
            f"",
            f"## 原始段落内容",
            f""
        ]

        # Show each paragraph as-is
        for idx, paragraph in enumerate(self.content, 1):
            markdown_lines.append(f"### 段落 {idx}")
            markdown_lines.append("")
            markdown_lines.append(paragraph)
            markdown_lines.append("")
            markdown_lines.append("---")
            markdown_lines.append("")

        return "\n".join(markdown_lines)

    def _convert_pdf_to_markdown(self) -> str:
        """Convert PDF pages to Markdown - raw page content."""
        markdown_lines = [
            f"# 文档内容: {self.file_path.name}",
            f"",
            f"**文件类型**: PDF",
            f"**页数**: {len(self.content)}",
            f"",
            f"---",
            f""
        ]

        # Show each page as-is
        for page_info in self.content:
            page_num = page_info['page']
            text = page_info['text']

            markdown_lines.append(f"## 第 {page_num} 页")
            markdown_lines.append("")
            markdown_lines.append("```")
            markdown_lines.append(text)
            markdown_lines.append("```")
            markdown_lines.append("")
            markdown_lines.append("---")
            markdown_lines.append("")

        return "\n".join(markdown_lines)

    def _convert_text_to_markdown(self) -> str:
        """Convert plain text to Markdown - raw text."""
        markdown_lines = [
            f"# 文档内容: {self.file_path.name}",
            f"",
            f"**文件类型**: 文本",
            f"",
            f"---",
            f"",
            f"## 原始文本内容",
            f"",
            f"```",
            self.content,
            f"```"
        ]

        return "\n".join(markdown_lines)

    def save_markdown(self, output_path: str = None) -> str:
        """Save Markdown to file."""
        markdown_content = self.convert_to_markdown()

        if output_path is None:
            # Use current working directory (caller's directory)
            output_path = Path.cwd() / (self.file_path.stem + "_for_analysis.md")
        else:
            output_path = Path(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return str(output_path)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_markdown.py <input_file> [output_file]")
        print("\nConverts documents to Markdown format for Claude analysis.")
        print("Preserves raw content without interpretation.")
        print("\nExample:")
        print("  python convert_to_markdown.py FAQ.xlsx")
        print("  python convert_to_markdown.py document.docx analysis.md")
        print("\nSupported formats: .xlsx, .docx, .pdf, .txt, .md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Convert to Markdown
    converter = DocumentToMarkdown(input_file)

    print(f"Loading {input_file}...")
    if not converter.load_document():
        sys.exit(1)

    print("Converting to Markdown (raw content)...")
    saved_path = converter.save_markdown(output_file)

    print(f"\n✓ Conversion complete!")
    print(f"✓ Markdown file saved to: {saved_path}")
    print(f"\nThe file contains the raw, unprocessed content.")
    print(f"Claude can now read and analyze it without any pre-interpretation.")
    print(f"\nNext steps:")
    print(f"  1. Review {saved_path} to see the raw content")
    print(f"  2. Ask Claude to analyze this file")
    print(f"  3. Claude will provide intelligent recommendations")


if __name__ == '__main__':
    main()
