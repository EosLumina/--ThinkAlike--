#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.services.documentation_sovereignty import DocumentationSovereigntyService

def main():
    parser = argparse.ArgumentParser(description="Documentation Sovereignty Tool")
    parser.add_argument("--generate", action="store_true", help="Generate integrity map")
    parser.add_argument("--verify", action="store_true", help="Verify documentation integrity")
    
    args = parser.parse_args()
    
    service = DocumentationSovereigntyService()
    
    if args.generate:
        print("Generating documentation integrity map...")
        result = service.generate_integrity_map()
        print("Integrity map generated")
    elif args.verify:
        print("Verifying documentation integrity...")
        result = service.verify_integrity()
        print("Verification complete")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
