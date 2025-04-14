#!/usr/bin/env python3
import os
import re
from pathlib import Path


def validate_markdown_links(file_path):
    """Validate markdown links in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all markdown links [text](url)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

    issues = []
    for text, url in links:
        if url.startswith('http'):
            continue

        # Handle absolute paths
        if url.startswith('/'):
            url = url[1:]

        # Handle relative paths
        target = Path(file_path).parent / url
        try:
            target = target.resolve()
            if not target.exists():
                issues.append(f"Broken link: [{text}]({url})")
        except Exception as e:
            issues.append(f"Invalid link: [{text}]({url}) - {str(e)}")

    if issues:
        print(f"\nIssues in {file_path}:")
        for issue in issues:
            print(f"- {issue}")


def main():
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("docs directory not found")
        return

    for file_path in docs_dir.rglob('*.md'):
        validate_markdown_links(file_path)


if __name__ == "__main__":
    main()
