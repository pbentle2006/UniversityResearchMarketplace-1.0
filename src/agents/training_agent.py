"""Training Agent for research best practices education and skill development."""

from typing import List, Dict, Any
from datetime import datetime

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class TrainingAgent(BaseAgent):
    """
    Training Agent for research best practices education and skill development.

    Capabilities:
    - Personalized learning pathway generation
    - Interactive tutorials on statistical methods
    - Best practice checklist generation
    - Common pitfall warnings and guidance
    - Discipline-specific methodology training
    - Reproducibility workshop materials
    - Mentorship matching
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Training Agent"
        self.description = "Research best practices education and skill development"
        self.capabilities = [
            "Learning pathway generation",
            "Statistical tutorials",
            "Best practice checklists",
            "Pitfall warnings",
            "Methodology training",
            "Mentorship matching",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze researcher's skill level and training needs.

        Args:
            data: Dictionary containing:
                - experience_level: str (beginner, intermediate, advanced)
                - completed_training: List of completed modules
                - skill_gaps: List of identified gaps
                - research_stage: str (planning, data_collection, analysis, writing)
                - tools_used: List of tools researcher uses

        Returns:
            AgentResult with training recommendations
        """
        findings = []
        score = 100.0

        # Extract data
        experience = data.get('experience_level', 'beginner')
        completed = data.get('completed_training', [])
        gaps = data.get('skill_gaps', [])
        stage = data.get('research_stage', 'planning')
        tools = data.get('tools_used', [])

        # Assess experience level
        if experience == 'beginner':
            findings.append(Finding(
                title="Beginner Researcher",
                description="Foundational training modules recommended.",
                severity=FindingSeverity.INFO,
                category="skill_level",
            ))
            score -= 10  # Room for growth
        elif experience == 'intermediate':
            findings.append(Finding(
                title="Intermediate Researcher",
                description="Advanced methods and best practices training available.",
                severity=FindingSeverity.INFO,
                category="skill_level",
            ))
        else:
            findings.append(Finding(
                title="Advanced Researcher",
                description="Specialized topics and mentoring opportunities available.",
                severity=FindingSeverity.SUCCESS,
                category="skill_level",
            ))

        # Check completed training
        core_modules = ['research_ethics', 'data_management', 'statistics_basics', 'reproducibility']
        completed_core = [m for m in core_modules if m in completed]

        if len(completed_core) == len(core_modules):
            findings.append(Finding(
                title="Core Training Complete",
                description="All core training modules completed.",
                severity=FindingSeverity.SUCCESS,
                category="training",
            ))
        elif len(completed_core) > 0:
            remaining = set(core_modules) - set(completed_core)
            findings.append(Finding(
                title="Core Training Incomplete",
                description=f"Complete remaining modules: {', '.join(remaining)}",
                severity=FindingSeverity.WARNING,
                category="training",
            ))
            score -= 10
        else:
            findings.append(Finding(
                title="Core Training Not Started",
                description="Begin with foundational training modules.",
                severity=FindingSeverity.WARNING,
                category="training",
            ))
            score -= 20

        # Check skill gaps
        if gaps:
            findings.append(Finding(
                title="Skill Gaps Identified",
                description=f"Training needed in: {', '.join(gaps[:3])}",
                severity=FindingSeverity.INFO,
                category="skills",
            ))

        # Stage-specific recommendations
        stage_findings = self._get_stage_findings(stage)
        findings.extend(stage_findings)

        # Tool proficiency
        essential_tools = self._get_essential_tools()
        missing_tools = [t for t in essential_tools if t not in tools]
        if missing_tools:
            findings.append(Finding(
                title="Tool Training Recommended",
                description=f"Consider learning: {', '.join(missing_tools[:3])}",
                severity=FindingSeverity.INFO,
                category="tools",
            ))

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
                "experience": experience,
                "completed_modules": len(completed),
                "skill_gaps": gaps,
                "stage": stage,
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate training recommendations."""
        recommendations = []

        for finding in analysis_result.findings:
            if "core training" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Complete Core Training",
                    description="Finish foundational modules for research best practices.",
                    priority=1,
                    action_items=[
                        "Complete Research Ethics module",
                        "Complete Data Management module",
                        "Complete Statistics Basics module",
                        "Complete Reproducibility module",
                    ],
                    resources=[
                        "Coursera: Research Data Management",
                        "edX: Introduction to Research Ethics",
                    ],
                ))

            if "beginner" in finding.title.lower():
                recommendations.append(Recommendation(
                    title="Start Learning Pathway",
                    description="Follow structured learning path for your research domain.",
                    priority=1,
                    action_items=[
                        "Take introductory statistics course",
                        "Learn version control with Git",
                        "Practice data visualization",
                        "Study research design principles",
                    ],
                    resources=[
                        "Software Carpentry workshops",
                        "DataCamp courses",
                    ],
                ))

        # Always recommend continuous learning
        recommendations.append(Recommendation(
            title="Stay Current",
            description="Keep up with methodological advances in your field.",
            priority=3,
            action_items=[
                "Follow relevant journals and preprints",
                "Attend conferences and workshops",
                "Join research methods communities",
                "Consider peer mentoring",
            ],
            resources=[],
        ))

        return recommendations

    def _get_stage_findings(self, stage: str) -> List[Finding]:
        """Get findings specific to research stage."""
        findings = []

        stage_info = {
            "planning": {
                "title": "Planning Stage",
                "description": "Focus on study design, pre-registration, and power analysis.",
                "resources": ["Pre-registration", "Power analysis", "Literature review"],
            },
            "data_collection": {
                "title": "Data Collection Stage",
                "description": "Focus on protocol adherence and data quality.",
                "resources": ["Data validation", "Protocol documentation", "Quality control"],
            },
            "analysis": {
                "title": "Analysis Stage",
                "description": "Focus on appropriate methods and reproducible workflows.",
                "resources": ["Statistical methods", "Code organization", "Version control"],
            },
            "writing": {
                "title": "Writing Stage",
                "description": "Focus on transparent reporting and documentation.",
                "resources": ["Reporting guidelines", "Data sharing", "Open science"],
            },
        }

        info = stage_info.get(stage, stage_info["planning"])

        findings.append(Finding(
            title=info["title"],
            description=info["description"],
            severity=FindingSeverity.INFO,
            category="stage",
            details={"resources": info["resources"]},
        ))

        return findings

    def _get_essential_tools(self) -> List[str]:
        """Get list of essential tools based on persona."""
        base_tools = ["Git", "Reference manager", "Spreadsheet"]

        persona_tools = {
            "climate": base_tools + ["Python", "NetCDF tools", "GIS"],
            "bio": base_tools + ["R", "Bioconductor", "BLAST"],
            "social": base_tools + ["SPSS/Stata", "NVivo", "Survey tools"],
            "data": base_tools + ["Python", "SQL", "Jupyter"],
        }

        return persona_tools.get(self.persona, base_tools + ["Python", "R"])

    def _get_status(self, score: float) -> str:
        """Get status string based on score."""
        if score >= 80:
            return "pass"
        elif score >= 60:
            return "warn"
        else:
            return "fail"

    def generate_learning_pathway(self, experience: str, persona: str) -> List[Dict[str, Any]]:
        """
        Generate personalized learning pathway.

        Args:
            experience: Experience level
            persona: Research persona

        Returns:
            List of learning modules in order
        """
        pathways = {
            "beginner": [
                {"module": "Research Ethics", "duration": "2 hours", "type": "required"},
                {"module": "Introduction to Statistics", "duration": "4 hours", "type": "required"},
                {"module": "Data Management Basics", "duration": "3 hours", "type": "required"},
                {"module": "Version Control with Git", "duration": "2 hours", "type": "required"},
                {"module": "Reproducibility Fundamentals", "duration": "2 hours", "type": "required"},
            ],
            "intermediate": [
                {"module": "Advanced Statistics", "duration": "4 hours", "type": "recommended"},
                {"module": "Pre-registration Workshop", "duration": "2 hours", "type": "required"},
                {"module": "Data Visualization", "duration": "3 hours", "type": "recommended"},
                {"module": "Code Review Practices", "duration": "2 hours", "type": "recommended"},
            ],
            "advanced": [
                {"module": "Bayesian Methods", "duration": "4 hours", "type": "optional"},
                {"module": "Meta-analysis", "duration": "3 hours", "type": "optional"},
                {"module": "Teaching Reproducibility", "duration": "2 hours", "type": "optional"},
                {"module": "Mentorship Skills", "duration": "2 hours", "type": "optional"},
            ],
        }

        return pathways.get(experience, pathways["beginner"])

    def generate_checklist(self, stage: str) -> List[Dict[str, Any]]:
        """
        Generate best practice checklist for research stage.

        Args:
            stage: Current research stage

        Returns:
            List of checklist items
        """
        checklists = {
            "planning": [
                {"item": "Conduct literature review", "status": "pending"},
                {"item": "Define research questions", "status": "pending"},
                {"item": "Perform power analysis", "status": "pending"},
                {"item": "Pre-register study", "status": "pending"},
                {"item": "Create data management plan", "status": "pending"},
                {"item": "Obtain ethics approval", "status": "pending"},
            ],
            "data_collection": [
                {"item": "Follow protocol exactly", "status": "pending"},
                {"item": "Document any deviations", "status": "pending"},
                {"item": "Perform data quality checks", "status": "pending"},
                {"item": "Back up data regularly", "status": "pending"},
                {"item": "Maintain audit trail", "status": "pending"},
            ],
            "analysis": [
                {"item": "Use version control", "status": "pending"},
                {"item": "Document analysis steps", "status": "pending"},
                {"item": "Check assumptions", "status": "pending"},
                {"item": "Report all analyses", "status": "pending"},
                {"item": "Calculate effect sizes", "status": "pending"},
                {"item": "Conduct sensitivity analyses", "status": "pending"},
            ],
            "writing": [
                {"item": "Follow reporting guidelines", "status": "pending"},
                {"item": "Disclose conflicts of interest", "status": "pending"},
                {"item": "Prepare data for sharing", "status": "pending"},
                {"item": "Create reproducible materials", "status": "pending"},
                {"item": "Write clear methods section", "status": "pending"},
            ],
        }

        return checklists.get(stage, checklists["planning"])

    def match_mentor(self, mentee_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Match mentee with potential mentors.

        Args:
            mentee_profile: Mentee's profile and needs

        Returns:
            List of potential mentor matches
        """
        # Mock mentor matching for prototype
        return [
            {
                "name": "Dr. Expert Mentor",
                "institution": "Research University",
                "expertise": mentee_profile.get('skill_gaps', ['General methods'])[0] if mentee_profile.get('skill_gaps') else 'General methods',
                "availability": "Weekly office hours",
                "match_score": 90,
            },
            {
                "name": "Prof. Senior Researcher",
                "institution": "Institute of Science",
                "expertise": "Research design",
                "availability": "Monthly meetings",
                "match_score": 85,
            },
        ]
