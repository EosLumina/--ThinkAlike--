from datetime import datetime
import hashlib
import json
import os
import git
from pathlib import Path
# Traceability import will be added when the service is implemented

class DocumentationSovereigntyService:
    """Service that embodies our radical transparency principle for documentation.
    
    This service ensures documentation sovereignty by:
    1. Tracking all changes to documentation
    2. Creating integrity proofs for verification
    3. Establishing clear provenance chains
    4. Preventing unauthorized modifications
    """

    def __init__(self, db=None, docs_dir=None, integrity_file=None):
        self.db = db
        self.docs_dir = docs_dir or Path('/workspaces/--ThinkAlike--/docs')
        self.integrity_file = integrity_file or Path('/workspaces/--ThinkAlike--/docs/INTEGRITY.json')
        self.traceability = TraceabilityService(db) if db else None

    def generate_integrity_map(self):
        """Create verifiable integrity proofs for all documentation."""
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
