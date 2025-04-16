"""
Novo𝝮 - The Newcomer's Companion

This guide welcomes new contributors regardless of technical
background, helping them find meaningful ways to contribute
to the ThinkAlike revolution.
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from .guide_system import GuidanceResponse, GuidanceContext, GuidePersona, ContributorSkillLevel


class ContributorPathway(str, Enum):
    """Different pathways for newcomers to contribute."""
    DOCUMENTATION = "documentation"           # Documentation and explanation
    CONCEPTUAL = "conceptual"                 # Philosophical and ethical thinking
    DESIGN = "design"                         # User interface and experience design
    TECHNICAL = "technical"                   # Code and implementation
    COMMUNITY = "community"                   # Community building and support
    TESTING = "testing"                       # Testing and validation


class ContributorBackground(str, Enum):
    """Different backgrounds newcomers might have."""
    TECHNICAL_DEVELOPER = "technical_developer"
    DESIGNER = "designer"
    CONTENT_CREATOR = "content_creator"
    ETHICIST = "ethicist"
    NON_TECHNICAL = "non_technical"


class EntryPathway(BaseModel):
    """A pathway for a newcomer to begin contributing."""
    suitable_for: List[ContributorBackground]
    pathway_name: str
    description: str
    first_steps: List[str]
    learning_resources: List[Dict[str, str]]
    mentor_connection: Optional[str] = None

    class Config:
        from_attributes = True


class NovoGuide:
    """
    Implementation of the Novo guide persona for newcomer onboarding.
    """

    def __init__(self):
        """Initialize the Novo guide with pathways for newcomers."""
        self.pathways = self._initialize_pathways()

    def _initialize_pathways(self) -> Dict[ContributorPathway, List[EntryPathway]]:
        """Initialize the entry pathways for different contributor types."""
        return {
            ContributorPathway.DOCUMENTATION: [
                EntryPathway(
                    suitable_for=[ContributorBackground.CONTENT_CREATOR,
                                  ContributorBackground.NON_TECHNICAL],
                    pathway_name="Documentation Explorer",
                    description="Help improve project documentation by finding gaps, inconsistencies, or areas needing clarification.",
                    first_steps=[
                        "Read the project overview in docs/README.md",
                        "Explore the docs directory and identify areas that could be clearer",
                        "Submit suggestions for improvement through GitHub issues"
                    ],
                    learning_resources=[
                        {"title": "Documentation Guide",
                            "url": "docs/guides/contributor_guides/documentation_guide.md"},
                        {"title": "Markdown Basics",
                            "url": "https://www.markdownguide.org/basic-syntax/"}
                    ]
                )
            ],
            ContributorPathway.CONCEPTUAL: [
                EntryPathway(
                    suitable_for=[ContributorBackground.ETHICIST,
                                  ContributorBackground.NON_TECHNICAL],
                    pathway_name="Ethical Principles Defender",
                    description="Help ensure that ThinkAlike's implementation aligns with its ethical principles.",
                    first_steps=[
                        "Read the ethical guidelines in docs/core/ethics/ethical_guidelines.md",
                        "Review recent changes to identify potential ethical considerations",
                        "Participate in discussions about ethical implications of features"
                    ],
                    learning_resources=[
                        {"title": "Ethical Guidelines",
                            "url": "docs/core/ethics/ethical_guidelines.md"},
                        {"title": "Enlightenment 2.0 Principles",
                            "url": "docs/core/enlightenment_2_0/enlightenment_2_0_principles.md"}
                    ]
                )
            ],
            ContributorPathway.TECHNICAL: [
                EntryPathway(
                    suitable_for=[ContributorBackground.TECHNICAL_DEVELOPER],
                    pathway_name="Backend Apprentice",
                    description="Learn backend development while contributing to ThinkAlike's FastAPI implementation.",
                    first_steps=[
                        "Set up the development environment following docs/guides/contributor_guides/getting_started.md",
                        "Complete the tutorial quest in backend/tutorials/quest_1.md",
                        "Fix a simple issue labeled 'good first issue' in the GitHub repository"
                    ],
                    learning_resources=[
                        {"title": "FastAPI Tutorial",
                            "url": "https://fastapi.tiangolo.com/tutorial/"},
                        {"title": "Backend Development Guide",
                            "url": "docs/guides/developer_guides/backend_api_guidelines.md"}
                    ]
                )
            ]
        }

    def generate_guidance(self, context: GuidanceContext) -> GuidanceResponse:
        """
        Generate newcomer guidance for the given context.
        """
        # Determine which type of pathway would be most relevant
        relevant_pathway = self._determine_relevant_pathway(context)
        pathways = self.pathways.get(relevant_pathway, [])

        # If we have pathways for this category, use the first one as a suggestion
        suggested_pathway = pathways[0] if pathways else None

        return GuidanceResponse(
            guide_persona=GuidePersona.NOVO,
            philosophical_context=self._get_philosophical_context(),
            practical_guidance=self._get_practical_guidance(
                context, suggested_pathway),
            technical_details=None,  # Novo focuses on accessibility over technical details
            code_examples=[],  # Similarly, code examples might be minimal for newcomers
            next_steps=self._get_next_steps(suggested_pathway),
            learning_resources=self._get_learning_resources(suggested_pathway)
        )

    def _determine_relevant_pathway(self, context: GuidanceContext) -> ContributorPathway:
        """Determine the most relevant pathway based on the context."""
        # This would be more sophisticated in a real implementation
        if context.specific_question:
            question = context.specific_question.lower()
            if any(kw in question for kw in ["document", "write", "explain", "clarify"]):
                return ContributorPathway.DOCUMENTATION
            elif any(kw in question for kw in ["ethics", "principles", "values", "philosophy"]):
                return ContributorPathway.CONCEPTUAL
            elif any(kw in question for kw in ["code", "develop", "implement", "program"]):
                return ContributorPathway.TECHNICAL

        # Default to documentation as an accessible entry point
        return ContributorPathway.DOCUMENTATION

    def _get_philosophical_context(self) -> str:
        """Generate philosophical context for newcomer guidance."""
        return (
            "Welcome to the digital liberation movement. ThinkAlike isn't merely software - "
            "it's a revolutionary approach to technology that respects human autonomy and collective wisdom. "
            "Your contribution, regardless of technical background, is essential to this mission. "
            "Like the ancient commons that sustained communities through shared stewardship, "
            "our digital commons flourishes through diverse participation and mutual aid."
        )

    def _get_practical_guidance(self, context: GuidanceContext, pathway: Optional[EntryPathway]) -> str:
        """Generate practical guidance for newcomers."""
        if pathway:
            return (
                f"Based on your interests, I recommend exploring the '{pathway.pathway_name}' pathway. "
                f"\n\n{pathway.description}\n\n"
                f"This pathway is perfect for contributors with {context.contributor_profile.skill_level.value} "
                f"technical background, requiring only: {', '.join(pathway.suitable_for)}."
            )
        else:
            return (
                "ThinkAlike welcomes contributors from all backgrounds. "
                "You can start by exploring the documentation in the docs/ directory, "
                "particularly the contributor guides in docs/guides/contributor_guides/. "
                "Don't worry about technical expertise - there are many ways to contribute "
                "beyond writing code."
            )

    def _get_next_steps(self, pathway: Optional[EntryPathway]) -> List[str]:
        """Generate next steps based on the suggested pathway."""
        return pathway.first_steps if pathway else [
            "Explore the docs directory to understand the project",
            "Join the community discussion on GitHub Discussions",
            "Find an area that interests you and reach out for guidance"
        ]

    def _get_learning_resources(self, pathway: Optional[EntryPathway]) -> List[Dict[str, str]]:
        """Provide learning resources based on the suggested pathway."""
        return pathway.learning_resources if pathway else [
            {"title": "Project Overview", "url": "docs/README.md"},
            {"title": "Contributor Guide",
                "url": "docs/guides/contributor_guides/getting_started.md"},
            {"title": "Ethical Guidelines",
                "url": "docs/core/ethics/ethical_guidelines.md"}
        ]
