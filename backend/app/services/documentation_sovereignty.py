import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Use a path relative to the project root
# Adjust the number based on your directory structure
# This should resolve to the repository root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Don't create directories at module level - move this to the class methods
# where it's actually needed to avoid initialization issues


class DocumentationSovereigntyService:
    """Service for verifying and maintaining documentation sovereignty.

    This service provides cryptographic integrity verification for documentation,
    ensuring the collective knowledge commons remains free from unauthorized
    modifications and establishing clear boundaries for conscious evolution.
    """

    def __init__(self, docs_dir=None, output_dir=None):
        # Use the PROJECT_ROOT constant for consistency
        self.repo_root = PROJECT_ROOT
        self.docs_dir = self.repo_root / \
            'docs' if docs_dir is None else Path(docs_dir)

        # Create data directory for integrity files if specified, otherwise use docs dir
        if output_dir is None:
            # Use a directory within the docs directory to ensure write permissions
            data_dir = self.docs_dir / 'integrity'
        else:
            data_dir = Path(output_dir)

        # Create the directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # Store integrity file in the appropriate location
        self.integrity_file = data_dir / 'INTEGRITY.json'

    def verify_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of all documentation against the stored integrity map.

        This function checks each documentation file against its recorded hash,
        identifying any unauthorized modifications or boundary violations.

        Returns:
            Dict containing verification results, including any integrity violations
        """
        # Initialize results structure
        results = {
            "verification_date": datetime.utcnow().isoformat(),
            "status": "verified",
            "violations": [],
            "stats": {
                "total_verified": 0,
                "total_violations": 0,
                "new_files": 0,
                "missing_files": 0,
                "modified_files": 0
            }
        }

        # Load integrity map if it exists, otherwise initialize empty map
        if os.path.exists(self.integrity_file):
            with open(self.integrity_file, 'r') as f:
                integrity_map = json.load(f)
        else:
            # First run, no integrity map exists
            return self.generate_integrity_map()

        # Check each file in the integrity map
        for rel_path, expected in integrity_map.get("documents", {}).items():
            doc_path = self.docs_dir / rel_path

            # Check if file exists
            if not os.path.exists(doc_path):
                results["violations"].append({
                    "file": rel_path,
                    "type": "missing",
                    "details": "File in integrity map is missing from documentation"
                })
                results["stats"]["missing_files"] += 1
                results["stats"]["total_violations"] += 1
                continue

            # Verify content hash
            with open(doc_path, 'rb') as f:
                content = f.read()
                current_hash = hashlib.sha256(content).hexdigest()

            if current_hash != expected["hash"]:
                results["violations"].append({
                    "file": rel_path,
                    "type": "modified",
                    "details": "Content hash doesn't match integrity map",
                    "expected_hash": expected["hash"],
                    "current_hash": current_hash
                })
                results["stats"]["modified_files"] += 1
                results["stats"]["total_violations"] += 1
            else:
                results["stats"]["total_verified"] += 1

        # Look for new files not in integrity map
        for doc_file in Path(self.docs_dir).glob('**/*.md'):
            # Skip files in hidden directories
            if any(part.startswith('.') for part in doc_file.parts):
                continue

            rel_path = str(doc_file.relative_to(self.docs_dir))
            if rel_path not in integrity_map.get("documents", {}):
                results["violations"].append({
                    "file": rel_path,
                    "type": "new",
                    "details": "File exists in documentation but not in integrity map"
                })
                results["stats"]["new_files"] += 1
                results["stats"]["total_violations"] += 1

        # Update overall status
        if results["stats"]["total_violations"] > 0:
            results["status"] = "violations_detected"

        return results

    def generate_integrity_map(self) -> Dict[str, Any]:
        """Generate cryptographic integrity map for all documentation.

        This creates a verifiable record of all documentation content that
        enables detection of unauthorized modifications and establishes
        clear provenance chains for collective knowledge.

        Returns:
            Dict containing the generated integrity map with cryptographic hashes
        """
        # Create a working integrity map
        integrity_map = {
            "generated_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "documents": {}
        }

        # Process each markdown file in the docs directory
        doc_count = 0

        # Use true relative paths that respect environment boundaries
        for doc_file in Path(self.docs_dir).glob('**/*.md'):
            # Skip files in hidden directories or files starting with .
            if any(part.startswith('.') for part in doc_file.parts) or doc_file.name.startswith('.'):
                continue

            # Use relative paths for cross-environment compatibility
            rel_path = str(doc_file.relative_to(self.docs_dir))

            # Generate cryptographic hash
            with open(doc_file, 'rb') as f:
                content = f.read()
                doc_hash = hashlib.sha256(content).hexdigest()

            # Store document integrity information
            integrity_map["documents"][rel_path] = {
                "hash": doc_hash,
                "last_updated": datetime.fromtimestamp(os.path.getmtime(doc_file)).isoformat(),
                "size_bytes": os.path.getsize(doc_file),
                "sovereignty_verified": True
            }

            doc_count += 1

        # Add statistics
        integrity_map["stats"] = {
            "document_count": doc_count,
            "verification_type": "cryptographic",
            "algorithm": "sha256"
        }

        # Ensure the parent directory exists with proper relative paths
        os.makedirs(self.docs_dir, exist_ok=True)

        # Write integrity map to file
        with open(self.integrity_file, 'w') as f:
            json.dump(integrity_map, f, indent=2)

        return integrity_map
