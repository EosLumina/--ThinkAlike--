#!/usr/bin/env python3
import os
import re
from pathlib import Path

LINK_REPLACEMENTS = {
    # Core documentation
    "../core/": "../../core/",
    "../../core/": "../core/",
    # Component documentation
    "../components/ui_components/": "../components/ui/",
    "../../components/ui_components/": "../../components/ui/",
    # Architecture documentation
    "../architecture/": "../../architecture/",
    "../../architecture/": "../architecture/",
    # Guide documentation
    "../guides/": "../../guides/",
    "../../guides/": "../guides/",
    # Template documentation
    "../templates/": "../../templates/",
    "../../templates/": "../templates/"
}


def fix_markdown_links(content):
    """Fix common link issues in markdown content."""
    for old, new in LINK_REPLACEMENTS.items():
        content = content.replace(old, new)

    # Fix absolute paths
    content = re.sub(r'\[([^\]]+)\]\(/docs/([^)]+)\)', r'[\1](../\2)', content)

    # Remove mailto links
    content = re.sub(r'\[([^]]+)\]\(mailto:[^)]+\)', r'\1', content)

    return content


def process_markdown_files():
    """Process all markdown files in docs directory."""
    docs_dir = Path('docs')
    if not docs_dir.exists():
        return

    for md_file in docs_dir.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            fixed_content = fix_markdown_links(content)

            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")


def on_pre_build(config):
    """MkDocs hook to run before build."""
    process_markdown_files()


if __name__ == "__main__":
    process_markdown_files()
