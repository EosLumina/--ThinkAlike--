#!/usr/bin/env python3
"""
Documentation CLI Tool

This script provides command-line tools for maintaining and updating
ThinkAlike documentation, supporting our principle of radical transparency.
"""

import argparse
import sys
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.documentation_service import DocumentationService


def update_api_docs(args):
    """Update API documentation."""
    doc_service = DocumentationService()
    updated_files = doc_service.update_api_documentation()
    
    if updated_files:
        print(f"Updated {len(updated_files)} API documentation files:")
        for file in updated_files:
            print(f"  - {file}")
    else:
        print("No API documentation files were updated.")


def update_model_docs(args):
    """Update model documentation."""
    doc_service = DocumentationService()
    updated_files = doc_service.update_model_documentation()
    
    if updated_files:
        print(f"Updated {len(updated_files)} model documentation files:")
        for file in updated_files:
            print(f"  - {file}")
    else:
        print("No model documentation files were updated.")


def update_links(args):
    """Update markdown links."""
    doc_service = DocumentationService()
    
    # Parse filename mapping from arguments
    filename_mapping = {}
    for mapping in args.mappings:
        old, new = mapping.split(':')
        filename_mapping[old] = new
    
    updated_files = doc_service.update_markdown_links(filename_mapping, args.directory)
    
    if updated_files:
        print(f"Updated links in {len(updated_files)} files:")
        for file, changes in updated_files.items():
            print(f"  - {file}:")
            for change in changes:
                print(f"    - {change}")
    else:
        print("No files were updated.")


def generate_api_summary(args):
    """Generate API summary."""
    doc_service = DocumentationService()
    summary_file = doc_service.generate_api_summary()
    
    print(f"Generated API summary: {summary_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='ThinkAlike Documentation Maintenance Tool')
    subparsers = parser.add_subparsers(dest='command', help='command to execute')
    
    # Update API docs command
    api_parser = subparsers.add_parser('update-api', help='Update API documentation')
    api_parser.set_defaults(func=update_api_docs)
    
    # Update model docs command
    model_parser = subparsers.add_parser('update-models', help='Update model documentation')
    model_parser.set_defaults(func=update_model_docs)
    
    # Update links command
    links_parser = subparsers.add_parser('update-links', help='Update markdown links')
    links_parser.add_argument(
        'mappings', 
        nargs='+', 
        help='Filename mappings in the format old:new'
    )
    links_parser.add_argument(
        '--directory', 
        '-d', 
        help='Directory to update (default: docs)'
    )
    links_parser.set_defaults(func=update_links)
    
    # Generate API summary command
    summary_parser = subparsers.add_parser('generate-summary', help='Generate API summary')
    summary_parser.set_defaults(func=generate_api_summary)
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()