#!/usr/bin/env python3

import os
from pathlib import Path


def main():
    # Ensure directories exist
    os.makedirs("/workspaces/--ThinkAlike--/backend/app/services", exist_ok=True)
    os.makedirs("/workspaces/--ThinkAlike--/scripts", exist_ok=True)
    os.makedirs("/workspaces/--ThinkAlike--/docs", exist_ok=True)
    Path("/workspaces/--ThinkAlike--/backend/__init__.py").touch()
    Path("/workspaces/--ThinkAlike--/backend/app/__init__.py").touch()
    Path("/workspaces/--ThinkAlike--/backend/app/services/__init__.py").touch()

    service_path = "/workspaces/--ThinkAlike--/backend/app/services/documentation_sovereignty.py"
    cli_path = "/workspaces/--ThinkAlike--/scripts/documentation_sovereignty.py"

    # Write service in chunks to avoid syntax errors
    service_content_part1 = """from datetime import datetime
import hashlib
import json
import os
import git
from pathlib import Path
from app.services.traceability_service import TraceabilityService

class DocumentationSovereigntyService:
    \"\"\"Service that embodies our radical transparency principle for documentation.
    
    This service ensures documentation sovereignty by:
    1. Tracking all changes to documentation
    2. Creating integrity proofs for verification
    3. Establishing clear provenance chains
    4. Preventing unauthorized modifications
    \"\"\"
"""
    service_content_part2 = """
    def __init__(self, db=None, docs_dir=None, integrity_file=None):
        self.db = db
        self.docs_dir = docs_dir or Path('/workspaces/--ThinkAlike--/docs')
        self.integrity_file = integrity_file or Path('/workspaces/--ThinkAlike--/docs/INTEGRITY.json')
        self.traceability = TraceabilityService(db) if db else None

    def generate_integrity_map(self):
        \"\"\"Create verifiable integrity proofs for all documentation.\"\"\"
        integrity_map = {
            "last_updated": datetime.utcnow().isoformat(),
            "documents": {}
        }
        
        # Process all markdown files
        for doc_file in self.docs_dir.glob('**/*.md'):
            relative_path = str(doc_file.relative_to(self.docs_dir))
"""
    service_content_part3 = r"""
            # Generate hash for integrity verification
            with open(doc_file, 'rb') as f:
                content = f.read()
                doc_hash = hashlib.sha256(content).hexdigest()
            
            # Get git history if available
            last_commit = None
            last_author = None
            try:
                repo = git.Repo(self.docs_dir, search_parent_directories=True)
                commits = list(repo.iter_commits(paths=str(doc_file), max_count=1))
                if commits:
                    last_commit = {
                        "id": str(commits[0].hexsha),
                        "date": datetime.fromtimestamp(commits[0].committed_date).isoformat(),
                        "message": commits[0].message
                    }
                    last_author = {
                        "name": commits[0].author.name,
                        "email": commits[0].author.email
                    }
            except (git.InvalidGitRepositoryError, git.NoSuchPathError):
                pass
            
            integrity_map["documents"][relative_path] = {
                "hash": doc_hash,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(doc_file)).isoformat(),
                "size_bytes": os.path.getsize(doc_file),
                "git_history": {
                    "last_commit": last_commit,
                    "last_author": last_author
                }
            }
        
        with open(self.integrity_file, 'w') as f:
            json.dump(integrity_map, f, indent=2)
        
        if self.traceability:
            self.traceability.record_data_creation(
                user_id="system",
                data_type="documentation_integrity_map",
                data_id=str(self.integrity_file),
                purpose="documentation_sovereignty"
            )
        
        return integrity_map
"""
    service_content_part4 = r"""
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
        
        for rel_path, expected in integrity_map["documents"].items():
            doc_file = self.docs_dir / rel_path
            if not doc_file.exists():
                results["violations"].append({
                    "file": rel_path,
                    "type": "missing",
                    "details": "Document no longer exists"
                })
                continue
            
            with open(doc_file, 'rb') as f:
                content = f.read()
                current_hash = hashlib.sha256(content).hexdigest()
            
            if current_hash != expected["hash"]:
                results["violations"].append({
                    "file": rel_path,
                    "type": "modified",
                    "details": "Content hash doesn't match integrity map"
                })
        
        for doc_file in self.docs_dir.glob('**/*.md'):
            rel_path = str(doc_file.relative_to(self.docs_dir))
            if rel_path not in integrity_map["documents"]:
                results.setdefault("new_files", []).append(rel_path)
        
        if results["violations"]:
            results["status"] = "integrity_violated"
        
        if self.traceability:
            self.traceability.record_data_access(
                user_id="system",
                data_type="documentation_integrity_verification",
                purpose="documentation_sovereignty"
            )
        
        return results
"""

    with open(service_path, "w") as f:
        f.write(service_content_part1)
        f.write(service_content_part2)
        f.write(service_content_part3)
        f.write(service_content_part4)

    print(f"Created {service_path}")

    cli_full_text = r"""#!/usr/bin/env python3
"""
    cli_full_text += r"""
"""
    cli_full_text += r"""
"""
    cli_full_text += r"""
import argparse
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.app.services.documentation_sovereignty import DocumentationSovereigntyService
except ImportError:
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
    docs_dir = Path(args.docs_dir) if args.docs_dir else None
    service = DocumentationSovereigntyService(docs_dir=docs_dir)
    
    if args.generate:
        print("Generating documentation integrity map...")
        result = service.generate_integrity_map()
        if 'documents' in result:
            print(f"✅ Integrity map generated with {len(result['documents'])} documents")
    elif args.verify:
        print("Verifying documentation integrity...")
        result = service.verify_integrity()
        if result['status'] == 'verified':
            print("✅ All documentation verified - sovereignty intact")
        elif result['status'] == 'integrity_violated':
            print("🚨 Documentation sovereignty violations detected:")
            for violation in result['violations']:
                print(f"  - {violation['file']}: {violation['type']} - {violation['details']}")
            if 'new_files' in result:
                print('\n📄 New files detected (not in integrity map):')
                for nf in result['new_files']:
                    print(f"  - {nf}")
            sys.exit(1)
    elif args.fix:
        print("Attempting to resolve documentation sovereignty issues...")
        service.generate_integrity_map()
        print("✅ New integrity map generated to incorporate changes")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
"""

    with open(cli_path, "w") as f:
        f.write(cli_full_text)

    print(f"Created {cli_path}")
    os.chmod(cli_path, 0o755)
    print(f"Made {cli_path} executable")


if __name__ == "__main__":
    main()
