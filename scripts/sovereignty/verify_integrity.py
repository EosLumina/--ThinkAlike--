#!/usr/bin/env python3
"""
Documentation Sovereignty CLI

A revolutionary tool for maintaining sovereignty over project documentation 
through cryptographic verification and provenance tracking.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from backend.app.services.documentation_sovereignty import DocumentationSovereigntyService
except ImportError:
    print("Error: Unable to import DocumentationSovereigntyService.")
    print("Ensure you've established the backend structure correctly.")
    sys.exit(1)


def format_file_size(size_bytes):
    """Format file size in a human-readable way."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def display_integrity_report(result, verbose=False):
    """Display integrity verification results in a clear, revolutionary format."""
    print(f"\n✦ Documentation Sovereignty Report ✦")
    print(f"  Verification Time: {result.get('verified_at', 'Unknown')}")

    stats = result.get("stats", {})
    print(f"  Documents Verified: {stats.get('total_verified', 0)}")
    print(f"  Integrity Violations: {stats.get('total_violations', 0)}")
    print(
        f"  New Untracked Files: {stats.get('new_files', 0) if 'new_files' in result else 0}")

    status = result.get("status", "unknown")
    if status == "verified":
        print("\n✅ All documentation verified - collective knowledge sovereignty intact")
    elif status == "integrity_violated":
        print("\n🚨 Documentation sovereignty violations detected:")
        for violation in result.get("violations", []):
            print(
                f"  - {violation['file']}: {violation['type']} - {violation['details']}")

        if "new_files" in result and result["new_files"]:
            print(
                f"\n📄 New files detected (not in integrity map): {len(result['new_files'])}")
            # Show up to 10 new files
            for i, new_file in enumerate(result["new_files"][:10]):
                print(f"  {i+1}. {new_file}")
            if len(result["new_files"]) > 10:
                print(f"  ... and {len(result['new_files']) - 10} more")
    elif status == "no_integrity_map":
        print("\n⚠️ No integrity map found. Generate one first with --generate")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Documentation Sovereignty Tool - Verify and maintain integrity of the knowledge commons",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Command line arguments
    parser.add_argument("--generate", action="store_true",
                        help="Generate integrity map for all documentation")
    parser.add_argument("--verify", action="store_true",
                        help="Verify documentation integrity against the map")
    parser.add_argument("--fix", action="store_true",
                        help="Regenerate integrity map to incorporate changes")
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    parser.add_argument("--docs-dir",
                        help="Path to docs directory (default: /workspaces/--ThinkAlike--/docs)")
    parser.add_argument("--history", metavar="FILE_PATH",
                        help="Show history for a specific document (relative path from docs root)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Display more detailed information")

    args = parser.parse_args()

    # Use provided docs directory or default
    docs_dir = Path(args.docs_dir) if args.docs_dir else None

    # Create service
    service = DocumentationSovereigntyService(docs_dir=docs_dir)

    if args.generate:
        print("Generating documentation integrity map...")
        result = service.generate_integrity_map()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✦ Documentation Integrity Map Generated ✦")
            print(f"  Total Documents: {result['stats']['total_documents']}")
            print(
                f"  Total Size: {format_file_size(result['stats']['total_size_bytes'])}")
            print(
                f"  Categories: {len(result['stats'].get('categories', {}))}")
            print("\n  The integrity map has been created at:")
            print(f"  {service.integrity_file}")
            print(
                "\n  This map establishes cryptographic verification for our knowledge commons,")
            print("  ensuring documentation remains free from unauthorized modification.")

    elif args.verify:
        print("Verifying documentation integrity...")
        result = service.verify_integrity()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            display_integrity_report(result, args.verbose)

        # Return non-zero exit code if integrity violations found
        if result["status"] == "integrity_violated":
            sys.exit(1)

    elif args.fix:
        print("Resolving documentation sovereignty issues...")
        result = service.generate_integrity_map()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("✅ New integrity map generated to incorporate changes")
            print(f"  Total Documents: {result['stats']['total_documents']}")
            print(
                f"  Total Size: {format_file_size(result['stats']['total_size_bytes'])}")

    elif args.history and hasattr(service, 'get_document_history'):
        print(f"Retrieving history for {args.history}...")
        result = service.get_document_history(args.history)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✦ Document History: {args.history} ✦")
            print(
                f"  Current Hash: {result.get('current_hash', 'Unknown')[:8]}...")
            print(
                f"  Integrity Status: {result.get('integrity_status', 'Unknown')}")
            print(f"  Last Modified: {result.get('last_modified', 'Unknown')}")
            print(f"  Size: {format_file_size(result.get('size_bytes', 0))}")

            if "git_history" in result and result["git_history"].get("commits"):
                print("\n📋 Commit History:")
                for i, commit in enumerate(result["git_history"]["commits"]):
                    author = commit.get("author", {}).get("name", "Unknown")
                    date = commit.get("date", "Unknown date")
                    msg = commit.get("message", "No message").split("\n")[0]
                    print(f"  {i+1}. [{date}] {author}: {msg}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
