#!/usr/bin/env python3
"""
ThinkAlike AI Guide Manager
--------------------------
The central coordinator for the constellation of specialized AI guides
that welcome newcomers and transform them into contributors regardless
of prior experience. This system democratizes participation by making
expert guidance available to all while teaching through contextual
assistance rather than requiring prior knowledge.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional, Union

# Define root project directory relative to this script
PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent.parent

# Guide domains represent different areas of expertise


class GuideDomain(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATA = "data"
    TESTING = "testing"
    DESIGN = "design"
    ETHICS = "ethics"
    GENERAL = "general"

# Learning paths for different journey types


class LearningPath(str, Enum):
    NEWCOMER = "newcomer"        # Complete beginners
    DEVELOPER = "developer"      # Experienced developers new to project
    DESIGNER = "designer"        # Design-focused contributors
    DOCUMENTER = "documenter"    # Documentation contributors
    TESTER = "tester"            # Testing-focused contributors
    REVOLUTIONARY = "revolutionary"  # Philosophical/ethical contributors

# Guide interaction modes


class InteractionMode(str, Enum):
    TERMINAL = "terminal"        # Command line interface
    WEB = "web"                  # Web-based interface
    IDE = "ide"                  # IDE integration (VSCode, etc.)
    DOCUMENTATION = "docs"       # Documentation site integration


class AIGuideManager:
    """
    Central management system for ThinkAlike's constellation of AI guides.

    This class orchestrates the different specialized guides, routes queries
    to the appropriate expert, and maintains context across interactions to
    provide a coherent learning and contribution experience.
    """

    def __init__(self):
        """Initialize the AI Guide Manager with available guides and paths."""
        self.guides_dir = PROJECT_ROOT / "tools" / "ai_guides"
        self.config_path = self.guides_dir / "config" / "guides_config.json"
        self.guides = self._load_guides()
        self.current_session = {
            "user": None,
            "path": None,
            "domain": None,
            "history": [],
            "learning_progress": {},
        }

    def _load_guides(self) -> Dict:
        """Load guide configurations from the config file."""
        if not self.config_path.exists():
            # Create default configuration if none exists
            return self._create_default_config()

        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading guides configuration: {e}")
            return self._create_default_config()

    def _create_default_config(self) -> Dict:
        """Create default configuration for guides."""
        default_config = {
            "guides": {
                "frontend": {
                    "name": "Frontend Guardian",
                    "description": "Guides through frontend development with React, TypeScript, and ThinkAlike UI principles",
                    "expertise": ["React", "TypeScript", "CSS", "UI Components", "State Management"],
                    "learning_paths": ["newcomer", "developer", "designer"],
                    "persona": "A creative and patient guide who illuminates the connection between code and user experience"
                },
                "backend": {
                    "name": "Backend Oracle",
                    "description": "Reveals the systems that power ThinkAlike's API, data processing, and service architecture",
                    "expertise": ["FastAPI", "SQLAlchemy", "Python", "API Design", "Database Modeling"],
                    "learning_paths": ["newcomer", "developer", "tester"],
                    "persona": "A methodical systems thinker who reveals the hidden patterns behind digital services"
                },
                "data": {
                    "name": "Data Alchemist",
                    "description": "Transforms raw information into meaningful structures while preserving privacy and ethics",
                    "expertise": ["Data Modeling", "ETL Processes", "Privacy Patterns", "Schema Design"],
                    "learning_paths": ["developer", "tester", "revolutionary"],
                    "persona": "A detail-oriented guardian of information who balances utility with respect for privacy"
                },
                "ethics": {
                    "name": "Ethics Explorer",
                    "description": "Guides contributors through the ethical principles of ThinkAlike and their implementation",
                    "expertise": ["Enlightenment 2.0", "Digital Ethics", "Privacy", "User Sovereignty"],
                    "learning_paths": ["newcomer", "revolutionary", "designer"],
                    "persona": "A philosophical navigator who connects technical decisions to their human impact"
                },
                "general": {
                    "name": "Path Illuminator",
                    "description": "Welcomes newcomers and helps them find their journey within ThinkAlike",
                    "expertise": ["Project Structure", "Contribution Workflow", "Community Norms"],
                    "learning_paths": ["newcomer", "developer", "designer", "documenter", "tester", "revolutionary"],
                    "persona": "A welcoming guide who helps contributors discover their unique place in the revolution"
                }
            },
            "learning_paths": {
                "newcomer": {
                    "name": "Newcomer Ascent",
                    "description": "From zero technical knowledge to making your first contribution",
                    "milestones": [
                        "Project setup and orientation",
                        "Understanding core concepts",
                        "First small contribution",
                        "Feedback and iteration",
                        "Regular contributor"
                    ]
                },
                "developer": {
                    "name": "Code Pilgrim",
                    "description": "For experienced developers to understand ThinkAlike's unique approach",
                    "milestones": [
                        "Technical environment setup",
                        "Architecture overview",
                        "Feature development workflow",
                        "Testing and quality assurance",
                        "Architectural contributions"
                    ]
                },
                "revolutionary": {
                    "name": "Digital Liberator",
                    "description": "For those focused on ethical principles and philosophical foundations",
                    "milestones": [
                        "Understanding Enlightenment 2.0",
                        "Analyzing ethical implications",
                        "Contributing to ethical guidelines",
                        "Implementing ethical principles in code",
                        "Advancing the philosophical framework"
                    ]
                }
            }
        }

        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # Save default configuration
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def start_session(self, username: str, path: Optional[LearningPath] = None,
                      domain: Optional[GuideDomain] = None):
        """Start a new guidance session for a user."""
        self.current_session = {
            "user": username,
            "path": path.value if path else None,
            "domain": domain.value if domain else None,
            "history": [],
            "learning_progress": {},
        }

        # Load existing user data if available
        user_data_path = self.guides_dir / "users" / f"{username}.json"
        if user_data_path.exists():
            try:
                with open(user_data_path, 'r') as f:
                    user_data = json.load(f)
                    self.current_session["learning_progress"] = user_data.get(
                        "learning_progress", {})
            except Exception as e:
                print(f"Error loading user data: {e}")

        return self._generate_welcome_message()

    def _generate_welcome_message(self) -> str:
        """Generate a personalized welcome message based on user context."""
        username = self.current_session["user"]
        path = self.current_session["path"]
        domain = self.current_session["domain"]

        # Select appropriate guide based on domain or use general guide
        guide_key = domain if domain and domain in self.guides["guides"] else "general"
        guide = self.guides["guides"][guide_key]

        # Build personalized welcome message
        message = f"Greetings, {username}! I am {guide['name']}, your guide to ThinkAlike.\n\n"

        if path and path in self.guides["learning_paths"]:
            path_info = self.guides["learning_paths"][path]
            message += f"You've chosen the {path_info['name']} journey: {path_info['description']}\n\n"

        message += guide["description"] + "\n\n"

        message += "How would you like to begin your revolutionary journey today?"

        return message

    def process_query(self, query: str) -> str:
        """Process a user query and return the appropriate guidance."""
        # Record the interaction in history
        self.current_session["history"].append(
            {"role": "user", "content": query})

        # Here we would implement routing logic to the appropriate specialized guide
        # For now, we'll implement a simple response system

        # Check if we need to pass this to a specialized domain guide
        domain = self.current_session["domain"]
        if not domain or domain == "general":
            # Determine which domain this query belongs to
            domain = self._determine_query_domain(query)

        # Get response from appropriate guide
        response = self._get_guide_response(domain, query)

        # Record the response in history
        self.current_session["history"].append(
            {"role": "guide", "content": response})

        return response

    def _determine_query_domain(self, query: str) -> str:
        """Determine which domain a query belongs to based on content analysis."""
        # This would ideally use a more sophisticated NLP approach
        # For now, we'll use a simple keyword matching system

        domain_keywords = {
            "frontend": ["react", "component", "css", "ui", "interface", "typescript", "jsx", "tsx"],
            "backend": ["api", "fastapi", "endpoint", "server", "database", "python", "sqlalchemy"],
            "data": ["data", "model", "schema", "privacy", "information", "structure"],
            "ethics": ["ethics", "privacy", "principles", "enlightenment", "sovereignty", "rights"],
            "testing": ["test", "quality", "assert", "pytest", "validation", "verify"]
        }

        # Count keyword matches for each domain
        domain_scores = {domain: 0 for domain in domain_keywords}
        query_lower = query.lower()

        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    domain_scores[domain] += 1

        # Get domain with highest score, defaulting to general if no strong match
        best_domain, best_score = max(
            domain_scores.items(), key=lambda x: x[1])
        return best_domain if best_score > 0 else "general"

    def _get_guide_response(self, domain: str, query: str) -> str:
        """Get response from the appropriate specialized guide."""
        # This would connect to the specialized guide implementation
        # For now, we'll use template responses

        if domain not in self.guides["guides"]:
            domain = "general"  # Default to general guide if domain not found

        guide = self.guides["guides"][domain]

        # Very basic response for demonstration
        response = f"As the {guide['name']}, I can help you with {query}.\n\n"

        # Add relevant expertise
        response += f"My areas of expertise include {', '.join(guide['expertise'])}.\n\n"

        # Add a placeholder for the actual guidance
        response += "To provide more specific guidance, I would need to understand your learning path and current progress better."

        return response

    def save_session(self):
        """Save the current session data for the user."""
        if not self.current_session["user"]:
            return

        user_dir = self.guides_dir / "users"
        os.makedirs(user_dir, exist_ok=True)

        user_data_path = user_dir / f"{self.current_session['user']}.json"

        try:
            with open(user_data_path, 'w') as f:
                json.dump(self.current_session, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def end_session(self) -> str:
        """End the current guidance session and save progress."""
        self.save_session()

        username = self.current_session["user"]
        farewell = f"Thank you for your revolutionary work today, {username}. Your progress has been saved, and I'll be here to guide you whenever you return."

        # Reset session
        self.current_session = {
            "user": None,
            "path": None,
            "domain": None,
            "history": [],
            "learning_progress": {},
        }

        return farewell


def main():
    """Command-line interface for the AI Guide Manager."""
    parser = argparse.ArgumentParser(description="ThinkAlike AI Guide Manager")
    parser.add_argument("--user", "-u", help="Username for the session")
    parser.add_argument("--path", "-p", help="Learning path",
                        choices=[p.value for p in LearningPath])
    parser.add_argument("--domain", "-d", help="Guide domain",
                        choices=[d.value for d in GuideDomain])
    parser.add_argument("--mode", "-m", help="Interaction mode",
                        choices=[m.value for m in InteractionMode], default="terminal")

    args = parser.parse_args()

    guide_manager = AIGuideManager()

    if not args.user:
        print("Please provide a username with --user or -u")
        sys.exit(1)

    # Convert string args to enums if provided
    path = LearningPath(args.path) if args.path else None
    domain = GuideDomain(args.domain) if args.domain else None

    # Start session
    welcome = guide_manager.start_session(args.user, path, domain)
    print(welcome)

    # Interactive terminal mode
    if args.mode == "terminal":
        print("\nType 'exit' or 'quit' to end the session.")
        while True:
            try:
                query = input("\n> ")
                if query.lower() in ["exit", "quit"]:
                    break

                response = guide_manager.process_query(query)
                print(f"\n{response}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    # End session
    farewell = guide_manager.end_session()
    print(f"\n{farewell}")


if __name__ == "__main__":
    main()
