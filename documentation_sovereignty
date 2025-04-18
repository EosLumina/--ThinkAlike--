from datetime import datetime
import hashlib
import json
import os
try:
    import git  # type: ignore
except ImportError:
    git = None  # Make git optional if not installed
from pathlib import Path
import sys
import argparse

# Add project root to path so we can import backend services if available
project_root = Path(__file__).resolve().parent
if project_root.name == 'scripts':
    project_root = project_root.parent
sys.path.insert(0, str(project_root))

# Attempt to import the real services, fall back to placeholders if needed
try:
    from backend.app.services.traceability_service import TraceabilityService as RealTraceabilityService
except ImportError:
    print("Warning: Real TraceabilityService not found, using placeholder.")
    class PlaceholderTraceabilityService:
        def __init__(self, db=None): pass
        def record_data_creation(self, **kwargs): pass
        def record_data_access(self, **kwargs): pass
    RealTraceabilityService = PlaceholderTraceabilityService

TraceabilityServiceType = RealTraceabilityService

try:
    from backend.app.services.documentation_sovereignty import DocumentationSovereigntyService as RealDocSovereigntyService
except ImportError:
    print("Warning: Real DocumentationSovereigntyService not found in backend.app.services, using local definition.")
    RealDocSovereigntyService = None

class LocalDocumentationSovereigntyService:
    """Service that embodies our radical transparency principle for documentation."""

    def __init__(self, db=None, docs_dir=None, integrity_file=None):
        self.db = db
        self.docs_dir = docs_dir if docs_dir is not None else (project_root / 'docs')
        self.integrity_file = integrity_file if integrity_file is not None else (self.docs_dir / 'INTEGRITY.json')
        self.traceability: TraceabilityServiceType = TraceabilityServiceType(db)

        if not self.docs_dir.exists():
            print(f"Warning: Documentation directory not found: {self.docs_dir}")
            self.docs_dir.mkdir(parents=True, exist_ok=True)

    def generate_integrity_map(self):
        """Create verifiable integrity proofs for all documentation."""
        integrity_map = {
            "last_updated": datetime.utcnow().isoformat(),
            "documents": {}
        }

        for doc_file in self.docs_dir.rglob('*.md'):
            if not doc_file.is_file(): continue
            if doc_file.resolve() == self.integrity_file.resolve():
                continue

            relative_path = str(doc_file.relative_to(self.docs_dir)).replace('\\', '/')

            try:
                with open(doc_file, 'rb') as f:
                    content = f.read()
                    doc_hash = hashlib.sha256(content).hexdigest()
            except Exception as e:
                print(f"Error reading file {doc_file}: {e}")
                continue

            last_commit = None
            last_author = None
            if git:
                try:
                    repo = git.Repo(self.docs_dir, search_parent_directories=True)
                    repo_root = Path(repo.working_dir)
                    repo_relative_path = str(doc_file.relative_to(repo_root)).replace('\\', '/')
                    commits = list(repo.iter_commits(paths=repo_relative_path, max_count=1))
                    if commits:
                        commit = commits[0]
                        last_commit = {
                            "id": str(commit.hexsha),
                            "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
                            "message": commit.message.strip()
                        }
                        last_author = {
                            "name": commit.author.name,
                            "email": commit.author.email
                        }
                except (git.InvalidGitRepositoryError, git.NoSuchPathError):
                    pass
                except Exception as e:
                    print(f"Error getting git history for {doc_file}: {e}")

            try:
                integrity_map["documents"][relative_path] = {
                    "hash": doc_hash,
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(doc_file)).isoformat(),
                    "size_bytes": os.path.getsize(doc_file),
                    "git_history": {
                        "last_commit": last_commit,
                        "last_author": last_author
                    }
                }
            except Exception as e:
                print(f"Error getting file metadata for {doc_file}: {e}")

        try:
            self.integrity_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.integrity_file, 'w') as f:
                json.dump(integrity_map, f, indent=2, sort_keys=True)
        except Exception as e:
            print(f"Error writing integrity map to {self.integrity_file}: {e}")
            return None

        self.traceability.record_data_creation(
            user_id="system",
            data_type="documentation_integrity_map",
            data_id=str(self.integrity_file.relative_to(project_root)),
            purpose="documentation_sovereignty"
        )

        return integrity_map

    def verify_integrity(self):
        """Verify all documentation against integrity map."""
        if not self.integrity_file.exists():
            return {"status": "no_integrity_map", "message": f"Integrity map not found: {self.integrity_file}"}

        try:
            with open(self.integrity_file, 'r') as f:
                integrity_map = json.load(f)
        except Exception as e:
            return {"status": "error", "message": f"Error reading integrity map {self.integrity_file}: {e}"}

        results = {
            "verified_at": datetime.utcnow().isoformat(),
            "status": "verified",
            "violations": [],
            "new_files": [],
            "checked_files": 0
        }
        found_files_in_map = set()

        for rel_path, expected in integrity_map.get("documents", {}).items():
            found_files_in_map.add(rel_path)
            doc_file = self.docs_dir / rel_path
            results["checked_files"] += 1

            if not doc_file.exists():
                results["violations"].append({
                    "file": rel_path,
                    "type": "missing",
                    "details": "Document listed in integrity map no longer exists"
                })
                continue

            try:
                with open(doc_file, 'rb') as f:
                    content = f.read()
                    current_hash = hashlib.sha256(content).hexdigest()
            except Exception as e:
                results["violations"].append({
                    "file": rel_path,
                    "type": "read_error",
                    "details": f"Could not read or hash file: {e}"
                })
                continue

            if current_hash != expected.get("hash"):
                results["violations"].append({
                    "file": rel_path,
                    "type": "modified",
                    "details": "Content hash doesn't match integrity map"
                })

        for doc_file in self.docs_dir.rglob('*.md'):
            if not doc_file.is_file(): continue
            if doc_file.resolve() == self.integrity_file.resolve():
                continue
            rel_path = str(doc_file.relative_to(self.docs_dir)).replace('\\', '/')
            if rel_path not in found_files_in_map:
                results["new_files"].append(rel_path)

        if results["violations"]:
            results["status"] = "integrity_violated"
        elif not integrity_map.get("documents"):
            has_md_files = any(self.docs_dir.rglob('*.md'))
            if has_md_files:
                results["status"] = "empty_map"
            else:
                results["status"] = "verified"
        elif not results["violations"] and not results["new_files"]:
            results["status"] = "verified"

        self.traceability.record_data_access(
            user_id="system",
            data_type="documentation_integrity_verification",
            purpose="documentation_sovereignty"
        )

        return results

DocumentationSovereigntyService = RealDocSovereigntyService if RealDocSovereigntyService else LocalDocumentationSovereigntyService

def cli_main():
    parser = argparse.ArgumentParser(description="Documentation Sovereignty Tool")
    parser.add_argument("--generate", action="store_true", help="Generate integrity map")
    parser.add_argument("--verify", action="store_true", help="Verify documentation integrity")
    parser.add_argument("--fix", action="store_true", help="Regenerate integrity map to fix discrepancies (use with caution)")
    parser.add_argument("--docs-dir", help="Path to docs directory (defaults to ./docs relative to project root)")
    parser.add_argument("--integrity-file", help="Path to integrity JSON file (defaults to ./docs/INTEGRITY.json)")

    args = parser.parse_args()

    docs_dir_path = Path(args.docs_dir).resolve() if args.docs_dir else (project_root / 'docs')
    integrity_file_path = Path(args.integrity_file).resolve() if args.integrity_file else (docs_dir_path / 'INTEGRITY.json')

    service = DocumentationSovereigntyService(docs_dir=docs_dir_path, integrity_file=integrity_file_path)

    if args.generate or args.fix:
        action = "Generating" if args.generate else "Regenerating (fixing)"
        print(f"{action} documentation integrity map for '{service.docs_dir}'...")
        result = service.generate_integrity_map()
        if result:
            print(f"✅ Integrity map {'generated' if args.generate else 'regenerated'} at '{service.integrity_file}' with {len(result.get('documents', {}))} documents")
        else:
            print(f"❌ Failed to {'generate' if args.generate else 'regenerate'} integrity map.")
            sys.exit(1)

    elif args.verify:
        print(f"Verifying documentation integrity using '{service.integrity_file}'...")
        result = service.verify_integrity()
        checked_count = result.get("checked_files", 0)

        if result["status"] == "verified":
            print(f"✅ All {checked_count} documentation file(s) verified - sovereignty intact")
            if result.get("new_files"):
                print("\n📄 New files detected (not yet tracked in integrity map):")
                for new_file in result["new_files"]:
                    print(f"  - {new_file}")
                print("\nRun with --generate to include these files.")

        elif result["status"] == "integrity_violated":
            print(f"🚨 Documentation sovereignty violations detected ({checked_count} file(s) checked):")
            for violation in result.get("violations", []):
                if isinstance(violation, dict):
                    file_path = violation.get('file', 'N/A')
                    violation_type = violation.get('type', 'N/A')
                    details = violation.get('details', 'N/A')
                    print(f"  - {file_path}: {violation_type} - {details}")
                else:
                    print(f"  - Invalid violation format: {violation}")

            if result.get("new_files"):
                print("\n📄 New files detected (not in integrity map):")
                for new_file in result["new_files"]:
                    print(f"  - {new_file}")
            print("\nRun with --fix to accept current state and regenerate the integrity map.")
            sys.exit(1)
        elif result["status"] == "no_integrity_map":
            print(f"❌ {result['message']}")
            print("Run with --generate to create one.")
            sys.exit(1)
        elif result["status"] == "empty_map":
            print(f"🟡 Integrity map '{service.integrity_file}' exists but contains no documents.")
            print("Run with --generate to populate it if documentation files exist.")
        elif result["status"] == "error":
            print(f"❌ {result['message']}")
            sys.exit(1)
        else:
            print(f"❓ Unknown verification status: {result['status']}")

    else:
        parser.print_help()

if __name__ == "__main__":
    if not git:
        print("Warning: GitPython is not installed or 'git' command not found. Git history will not be recorded.")
        print("Install it with: pip install GitPython")
    cli_main()
