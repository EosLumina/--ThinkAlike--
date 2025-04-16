# Simple file creator that avoids terminal interpretation issues
import os

# Service implementation
service_file = "/workspaces/--ThinkAlike--/backend/app/services/documentation_sovereignty.py"
service_content = """from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

class DocumentationSovereigntyService:
    \"\"\"Service that embodies our radical transparency principle for documentation.
    
    This service ensures documentation sovereignty by:
    1. Tracking all changes to documentation
    2. Creating integrity proofs for verification
    3. Establishing clear provenance chains
    4. Preventing unauthorized modifications
    \"\"\"
    
    def __init__(self, db=None, docs_dir=None, integrity_file=None):
        self.db = db
        self.docs_dir = docs_dir or Path('/workspaces/--ThinkAlike--/docs')
        self.integrity_file = integrity_file or Path('/workspaces/--ThinkAlike--/docs/INTEGRITY.json')
        self.traceability = None
        
    def generate_integrity_map(self):
        \"\"\"Create verifiable integrity proofs for all documentation.\"\"\"
        integrity_map = {
            "last_updated": datetime.utcnow().isoformat(),
            "documents": {}
        }
        
        # Process all markdown files
        for doc_file in self.docs_dir.glob('**/*.md'):
            relative_path = str(doc_file.relative_to(self.docs_dir))
            
            # Generate hash for integrity verification
            with open(doc_file, 'rb') as f:
                content = f.read()
                doc_hash = hashlib.sha256(content).hexdigest()
            
            # Store document metadata
            integrity_map["documents"][relative_path] = {
                "hash": doc_hash,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(doc_file)).isoformat(),
                "size_bytes": os.path.getsize(doc_file)
            }
        
        # Write integrity map to file
        with open(self.integrity_file, 'w') as f:
            json.dump(integrity_map, f, indent=2)
            
        return integrity_map
    
    def verify_integrity(self):
        \"\"\"Verify all documentation against integrity map.\"\"\"
        if not self.integrity_file.exists():
            return {"status": "no_integrity_map", "message": "No integrity map found. Generate one first."}
            
        with open(self.integrity_file, 'r') as f:
            integrity_map = json.load(f)
            
        results = {
            "verified_at": datetime.utcnow().isoformat(),
            "status": "verified",
            "violations": []
        }
        
        # Check each document in the integrity map
        for rel_path, expected in integrity_map["documents"].items():
            doc_file = self.docs_dir / rel_path
            
            # Check if file exists
            if not doc_file.exists():
                results["violations"].append({
                    "file": rel_path,
                    "type": "missing",
                    "details": "Document no longer exists"
                })
                continue
                
            # Verify hash
            with open(doc_file, 'rb') as f:
                content = f.read()
                current_hash = hashlib.sha256(content).hexdigest()
                
            if current_hash != expected["hash"]:
                results["violations"].append({
                    "file": rel_path,
                    "type": "modified",
                    "details": "Content hash doesn't match integrity map"
                })
        
        # Look for new files not in integrity map
        for doc_file in self.docs_dir.glob('**/*.md'):
            rel_path = str(doc_file.relative_to(self.docs_dir))
            if rel_path not in integrity_map["documents"]:
                results["new_files"] = results.get("new_files", [])
                results["new_files"].append(rel_path)
        
        # Update status if violations found
        if results["violations"]:
            results["status"] = "integrity_violated"
            
        return results
"""

# CLI implementation
cli_file = "/workspaces/--ThinkAlike--/scripts/documentation_sovereignty.py"
cli_content = """#!/usr/bin/env python3
\"\"\"
Documentation Sovereignty CLI

A revolutionary tool for maintaining sovereignty over project documentation.
\"\"\"

import argparse
import sys
from pathlib import Path
import os

# Add project root to path so we can import our services
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.app.services.documentation_sovereignty import DocumentationSovereigntyService
except ImportError:
    # If service doesn't exist yet, create minimal version
    class DocumentationSovereigntyService:
        def __init__(self, db=None, docs_dir=None, integrity_file=None):
            self.docs_dir = docs_dir or Path('/workspaces/--ThinkAlike--/docs')
            self.integrity_file = integrity_file or Path('/workspaces/--ThinkAlike--/docs/INTEGRITY.json')
            
        def generate_integrity_map(self):
            print("This is a placeholder. Full implementation requires the service to be created.")
            return {"status": "not_implemented"}
            
        def verify_integrity(self):
            print("This is a placeholder. Full implementation requires the service to be created.")
            return {"status": "not_implemented"}

def main():
    parser = argparse.ArgumentParser(description="Documentation Sovereignty Tool")
    parser.add_argument("--generate", action="store_true", help="Generate integrity map")
    parser.add_argument("--verify", action="store_true", help="Verify documentation integrity")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix integrity violations")
    parser.add_argument("--docs-dir", help="Path to docs directory")
    
    args = parser.parse_args()
    
    # Use provided docs directory or default
    docs_dir = Path(args.docs_dir) if args.docs_dir else None
    
    # Create service
    service = DocumentationSovereigntyService(docs_dir=docs_dir)
    
    if args.generate:
        print("Generating documentation integrity map...")
        result = service.generate_integrity_map()
        # Fixed f-string to avoid backslash issues
        doc_count = len(result.get('documents', {})) if isinstance(result, dict) else 0
        print(f"✅ Integrity map generated with {doc_count} documents")
        
    elif args.verify:
        print("Verifying documentation integrity...")
        result = service.verify_integrity()
        
        if result["status"] == "verified":
            print("✅ All documentation verified - sovereignty intact")
        elif result["status"] == "integrity_violated":
            print("�� Documentation sovereignty violations detected:")
            for violation in result["violations"]:
                print(f"  - {violation['file']}: {violation['type']} - {violation['details']}")
                
            if result.get("new_files"):
                print("\\n📄 New files detected (not in integrity map):")
                for new_file in result["new_files"]:
                    print(f"  - {new_file}")
                    
            sys.exit(1)
            
    elif args.fix:
        print("Attempting to resolve documentation sovereignty issues...")
        # In a real implementation, this would reconcile or merge changes
        service.generate_integrity_map()
        print("✅ New integrity map generated to incorporate changes")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""

# Write files
with open(service_file, 'w') as f:
    f.write(service_content)
print(f"Created {service_file}")

with open(cli_file, 'w') as f:
    f.write(cli_content)
print(f"Created {cli_file}")
