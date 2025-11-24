"""Collaboration Agent for team coordination and peer review."""

from typing import List, Dict, Any
from datetime import datetime

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class CollaborationAgent(BaseAgent):
    """
    Collaboration Agent for team coordination, peer review, and knowledge sharing.

    Capabilities:
    - Intelligent reviewer matching
    - Real-time collaboration coordination
    - Version control and contribution tracking
    - Conflict resolution facilitation
    - Cross-institutional partnership recommendations
    - Communication and milestone tracking
    - Credit and attribution management
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Collaboration Agent"
        self.description = "Team coordination, peer review, and knowledge sharing"
        self.capabilities = [
            "Reviewer matching",
            "Collaboration coordination",
            "Contribution tracking",
            "Partnership recommendations",
            "Milestone tracking",
            "Attribution management",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze collaboration and team dynamics.

        Args:
            data: Dictionary containing:
                - team_size: Number of team members
                - institutions: List of institutions involved
                - has_contribution_guidelines: Boolean
                - has_authorship_agreement: Boolean
                - communication_tools: List of tools used
                - has_project_timeline: Boolean
                - has_data_sharing_agreement: Boolean

        Returns:
            AgentResult with collaboration analysis
        """
        findings = []
        score = 100.0

        # Extract data
        team_size = data.get('team_size', 1)
        institutions = data.get('institutions', [])
        has_contrib_guidelines = data.get('has_contribution_guidelines', False)
        has_authorship = data.get('has_authorship_agreement', False)
        comm_tools = data.get('communication_tools', [])
        has_timeline = data.get('has_project_timeline', False)
        has_data_agreement = data.get('has_data_sharing_agreement', False)

        # Analyze team composition
        if team_size == 1:
            findings.append(Finding(
                title="Solo Researcher",
                description="Consider collaborating with others for diverse perspectives and peer review.",
                severity=FindingSeverity.INFO,
                category="team",
            ))
        elif team_size <= 5:
            findings.append(Finding(
                title="Small Team",
                description=f"Team of {team_size} members is manageable. Ensure clear role definitions.",
                severity=FindingSeverity.SUCCESS,
                category="team",
            ))
        else:
            findings.append(Finding(
                title="Large Team",
                description=f"Team of {team_size} members requires strong coordination structures.",
                severity=FindingSeverity.INFO,
                category="team",
            ))

        # Check multi-institutional collaboration
        if len(institutions) > 1:
            findings.append(Finding(
                title="Multi-Institutional Collaboration",
                description=f"Collaborating across {len(institutions)} institutions. Ensure data sharing agreements.",
                severity=FindingSeverity.INFO,
                category="collaboration",
            ))

            if not has_data_agreement:
                findings.append(Finding(
                    title="No Data Sharing Agreement",
                    description="Multi-institutional projects need formal data sharing agreements.",
                    severity=FindingSeverity.WARNING,
                    category="legal",
                ))
                score -= 15

        # Check contribution guidelines
        if team_size > 1:
            if has_contrib_guidelines:
                findings.append(Finding(
                    title="Contribution Guidelines Present",
                    description="Team has documented contribution guidelines.",
                    severity=FindingSeverity.SUCCESS,
                    category="process",
                ))
            else:
                findings.append(Finding(
                    title="No Contribution Guidelines",
                    description="Create guidelines for code contributions and review process.",
                    severity=FindingSeverity.WARNING,
                    category="process",
                ))
                score -= 10

        # Check authorship agreement
        if team_size > 1:
            if has_authorship:
                findings.append(Finding(
                    title="Authorship Agreement Present",
                    description="Team has agreed on authorship criteria.",
                    severity=FindingSeverity.SUCCESS,
                    category="attribution",
                ))
            else:
                findings.append(Finding(
                    title="No Authorship Agreement",
                    description="Establish authorship criteria early to prevent disputes.",
                    severity=FindingSeverity.WARNING,
                    category="attribution",
                ))
                score -= 10

        # Check communication
        if comm_tools:
            findings.append(Finding(
                title="Communication Tools Defined",
                description=f"Team uses: {', '.join(comm_tools)}",
                severity=FindingSeverity.SUCCESS,
                category="communication",
            ))
        else:
            if team_size > 1:
                findings.append(Finding(
                    title="No Communication Tools",
                    description="Define communication channels for the team.",
                    severity=FindingSeverity.WARNING,
                    category="communication",
                ))
                score -= 5

        # Check timeline
        if has_timeline:
            findings.append(Finding(
                title="Project Timeline Present",
                description="Project has defined milestones and timeline.",
                severity=FindingSeverity.SUCCESS,
                category="planning",
            ))
        else:
            findings.append(Finding(
                title="No Project Timeline",
                description="Create a timeline with milestones for project tracking.",
                severity=FindingSeverity.INFO,
                category="planning",
            ))
            score -= 5

        # Generate recommendations
        recommendations = self.get_recommendations(
            AgentResult(
                score=score,
                status=self._get_status(score),
                findings=findings,
                recommendations=[],
                metadata={},
            )
        )

        score = max(0, min(100, score))

        return AgentResult(
            score=score,
            status=self._get_status(score),
            findings=findings,
            recommendations=recommendations,
            metadata={
                "team_size": team_size,
                "num_institutions": len(institutions),
                "has_authorship": has_authorship,
                "has_contrib_guidelines": has_contrib_guidelines,
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate recommendations for collaboration improvement."""
        recommendations = []

        for finding in analysis_result.findings:
            if "authorship" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Establish Authorship Agreement",
                    description="Define authorship criteria using ICMJE guidelines or CRediT taxonomy.",
                    priority=1,
                    action_items=[
                        "Review ICMJE authorship criteria",
                        "Discuss authorship order expectations",
                        "Document contributions using CRediT taxonomy",
                        "Create written agreement signed by all team members",
                    ],
                    resources=[
                        "ICMJE Authorship Guidelines",
                        "CRediT Contributor Roles Taxonomy",
                    ],
                ))

            if "data sharing" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Create Data Sharing Agreement",
                    description="Formalize data sharing terms for multi-institutional collaboration.",
                    priority=1,
                    action_items=[
                        "Consult institutional legal/contracts office",
                        "Define data access permissions",
                        "Specify data retention and destruction policies",
                        "Address IP and publication rights",
                    ],
                    resources=[],
                ))

            if "contribution" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Create Contribution Guidelines",
                    description="Document how team members should contribute to the project.",
                    priority=2,
                    action_items=[
                        "Define code style and documentation standards",
                        "Establish code review process",
                        "Create pull request template",
                        "Document branching strategy",
                    ],
                    resources=[
                        "CONTRIBUTING.md templates",
                    ],
                ))

        # Always recommend regular check-ins
        recommendations.append(Recommendation(
            title="Schedule Regular Check-ins",
            description="Hold regular team meetings to ensure alignment and address issues.",
            priority=3,
            action_items=[
                "Set recurring meeting schedule",
                "Create shared agenda document",
                "Rotate meeting facilitator role",
                "Document decisions and action items",
            ],
            resources=[],
        ))

        return recommendations

    def _get_status(self, score: float) -> str:
        """Get status string based on score."""
        if score >= 80:
            return "pass"
        elif score >= 60:
            return "warn"
        else:
            return "fail"

    def match_reviewers(self, project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Match potential reviewers based on project characteristics.

        Args:
            project_data: Project information for matching

        Returns:
            List of potential reviewer matches
        """
        # Mock reviewer matching for prototype
        persona = self.persona or "data"

        reviewer_pool = {
            "climate": [
                {"name": "Dr. Sarah Chen", "institution": "Stanford", "expertise": "Climate modeling", "match_score": 92},
                {"name": "Prof. Michael Torres", "institution": "MIT", "expertise": "Atmospheric science", "match_score": 88},
            ],
            "bio": [
                {"name": "Dr. Emily Watson", "institution": "Harvard", "expertise": "Genomics", "match_score": 95},
                {"name": "Prof. James Kim", "institution": "UCSF", "expertise": "Biostatistics", "match_score": 87},
            ],
            "social": [
                {"name": "Dr. Maria Garcia", "institution": "Berkeley", "expertise": "Social psychology", "match_score": 91},
                {"name": "Prof. David Lee", "institution": "Columbia", "expertise": "Behavioral economics", "match_score": 85},
            ],
            "data": [
                {"name": "Dr. Alex Johnson", "institution": "CMU", "expertise": "Machine learning", "match_score": 93},
                {"name": "Prof. Lisa Wang", "institution": "Stanford", "expertise": "Statistics", "match_score": 89},
            ],
        }

        return reviewer_pool.get(persona, reviewer_pool["data"])

    def suggest_collaborators(self, research_interests: List[str]) -> List[Dict[str, Any]]:
        """
        Suggest potential collaborators based on research interests.

        Args:
            research_interests: List of research interest keywords

        Returns:
            List of potential collaborators
        """
        # Mock collaborator suggestions for prototype
        return [
            {
                "name": "Research Group Alpha",
                "institution": "MIT",
                "overlap_score": 85,
                "complementary_skills": ["Statistical methods", "Data visualization"],
            },
            {
                "name": "Dr. Research Partner",
                "institution": "Stanford",
                "overlap_score": 78,
                "complementary_skills": ["Domain expertise", "Grant writing"],
            },
        ]
