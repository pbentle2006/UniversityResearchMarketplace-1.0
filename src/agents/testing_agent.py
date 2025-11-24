"""Testing Agent for experimental design validation and reproducibility."""

from typing import List, Dict, Any

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class TestingAgent(BaseAgent):
    """
    Testing Agent for experimental design validation and reproducibility testing.

    Capabilities:
    - Experimental design review and optimization
    - Control group adequacy assessment
    - Randomization and blinding verification
    - Protocol deviation detection
    - Cross-validation and replication simulation
    - Environment reproducibility checking
    - Computational notebook validation
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Testing Agent"
        self.description = "Experimental design validation and reproducibility testing"
        self.capabilities = [
            "Experimental design review",
            "Control group assessment",
            "Randomization verification",
            "Protocol deviation detection",
            "Reproducibility checking",
            "Environment validation",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze experimental design and reproducibility.

        Args:
            data: Dictionary containing:
                - has_control_group: Boolean
                - is_randomized: Boolean
                - is_blinded: Boolean (single/double/none)
                - has_protocol: Boolean
                - environment_documented: Boolean
                - dependencies_locked: Boolean
                - has_tests: Boolean
                - code_reviewed: Boolean

        Returns:
            AgentResult with experimental design findings
        """
        findings = []
        score = 100.0

        # Extract data with defaults
        has_control = data.get('has_control_group', False)
        is_randomized = data.get('is_randomized', False)
        blinding = data.get('is_blinded', 'none')
        has_protocol = data.get('has_protocol', False)
        env_documented = data.get('environment_documented', False)
        deps_locked = data.get('dependencies_locked', False)
        has_tests = data.get('has_tests', False)
        code_reviewed = data.get('code_reviewed', False)

        # Check control group
        if has_control:
            findings.append(Finding(
                title="Control Group Present",
                description="Study includes appropriate control group for comparison.",
                severity=FindingSeverity.SUCCESS,
                category="experimental_design",
            ))
        else:
            findings.append(Finding(
                title="No Control Group",
                description="Consider adding a control group to strengthen causal inference.",
                severity=FindingSeverity.WARNING,
                category="experimental_design",
            ))
            score -= 15

        # Check randomization
        if is_randomized:
            findings.append(Finding(
                title="Randomization Applied",
                description="Participants/samples were randomized to conditions.",
                severity=FindingSeverity.SUCCESS,
                category="experimental_design",
            ))
        else:
            findings.append(Finding(
                title="No Randomization",
                description="Non-randomized design may introduce selection bias.",
                severity=FindingSeverity.WARNING,
                category="experimental_design",
            ))
            score -= 10

        # Check blinding
        if blinding == 'double':
            findings.append(Finding(
                title="Double-Blind Design",
                description="Both participants and researchers are blinded to conditions.",
                severity=FindingSeverity.SUCCESS,
                category="experimental_design",
            ))
        elif blinding == 'single':
            findings.append(Finding(
                title="Single-Blind Design",
                description="Participants are blinded to conditions. Consider double-blinding if feasible.",
                severity=FindingSeverity.INFO,
                category="experimental_design",
            ))
        else:
            findings.append(Finding(
                title="No Blinding",
                description="Open-label design may introduce bias. Consider blinding if feasible.",
                severity=FindingSeverity.WARNING,
                category="experimental_design",
            ))
            score -= 10

        # Check protocol
        if has_protocol:
            findings.append(Finding(
                title="Protocol Documented",
                description="Experimental protocol is documented for reproducibility.",
                severity=FindingSeverity.SUCCESS,
                category="reproducibility",
            ))
        else:
            findings.append(Finding(
                title="No Protocol Documentation",
                description="Document experimental protocol for reproducibility.",
                severity=FindingSeverity.WARNING,
                category="reproducibility",
            ))
            score -= 10

        # Check computational reproducibility
        if env_documented:
            findings.append(Finding(
                title="Environment Documented",
                description="Computational environment (OS, versions) is documented.",
                severity=FindingSeverity.SUCCESS,
                category="computational",
            ))
        else:
            findings.append(Finding(
                title="Environment Not Documented",
                description="Document your computational environment for reproducibility.",
                severity=FindingSeverity.WARNING,
                category="computational",
            ))
            score -= 10

        if deps_locked:
            findings.append(Finding(
                title="Dependencies Locked",
                description="Package dependencies are locked to specific versions.",
                severity=FindingSeverity.SUCCESS,
                category="computational",
            ))
        else:
            findings.append(Finding(
                title="Dependencies Not Locked",
                description="Lock dependencies with requirements.txt, environment.yml, or similar.",
                severity=FindingSeverity.WARNING,
                category="computational",
            ))
            score -= 5

        # Check testing
        if has_tests:
            findings.append(Finding(
                title="Tests Present",
                description="Code includes tests for validation.",
                severity=FindingSeverity.SUCCESS,
                category="code_quality",
            ))
        else:
            findings.append(Finding(
                title="No Tests",
                description="Add tests to validate analysis code correctness.",
                severity=FindingSeverity.INFO,
                category="code_quality",
            ))
            score -= 5

        # Check code review
        if code_reviewed:
            findings.append(Finding(
                title="Code Reviewed",
                description="Analysis code has been reviewed by another researcher.",
                severity=FindingSeverity.SUCCESS,
                category="code_quality",
            ))
        else:
            findings.append(Finding(
                title="Code Not Reviewed",
                description="Have another researcher review your analysis code.",
                severity=FindingSeverity.INFO,
                category="code_quality",
            ))

        # Persona-specific checks
        if self.persona == "bio":
            findings.append(Finding(
                title="Biological Replicates",
                description="Ensure adequate biological replicates, not just technical replicates.",
                severity=FindingSeverity.INFO,
                category="experimental_design",
            ))
        elif self.persona == "data":
            findings.append(Finding(
                title="Train/Test Split",
                description="Ensure proper separation of training and test data.",
                severity=FindingSeverity.INFO,
                category="methodology",
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
                "has_control": has_control,
                "is_randomized": is_randomized,
                "blinding": blinding,
                "env_documented": env_documented,
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate recommendations for experimental design improvement."""
        recommendations = []

        for finding in analysis_result.findings:
            if "control" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Add Control Group",
                    description="Include appropriate control conditions for comparison.",
                    priority=1,
                    action_items=[
                        "Identify appropriate control condition",
                        "Match controls on relevant variables",
                        "Ensure adequate control group size",
                    ],
                    resources=[],
                ))

            if "environment" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Document Computational Environment",
                    description="Record all software versions and system specifications.",
                    priority=2,
                    action_items=[
                        "Create requirements.txt or environment.yml",
                        "Document OS and hardware specifications",
                        "Consider using Docker for full reproducibility",
                    ],
                    resources=[
                        "Docker for reproducible research",
                        "conda environment management",
                    ],
                ))

        # Always recommend version control
        recommendations.append(Recommendation(
            title="Use Version Control for Protocols",
            description="Track changes to experimental protocols using version control.",
            priority=3,
            action_items=[
                "Store protocols in Git repository",
                "Document any protocol deviations",
                "Use semantic versioning for major changes",
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

    def validate_computational_reproducibility(self, data: Dict[str, Any]) -> List[Finding]:
        """
        Validate computational reproducibility aspects.

        Args:
            data: Computational environment data

        Returns:
            List of findings about reproducibility
        """
        findings = []

        # Check for random seeds
        if data.get('random_seed_set', False):
            findings.append(Finding(
                title="Random Seed Set",
                description="Random seed is set for reproducible results.",
                severity=FindingSeverity.SUCCESS,
                category="reproducibility",
            ))
        else:
            findings.append(Finding(
                title="Random Seed Not Set",
                description="Set random seeds for reproducible results.",
                severity=FindingSeverity.WARNING,
                category="reproducibility",
            ))

        # Check for absolute paths
        if not data.get('has_absolute_paths', False):
            findings.append(Finding(
                title="No Absolute Paths",
                description="Code uses relative paths for portability.",
                severity=FindingSeverity.SUCCESS,
                category="reproducibility",
            ))
        else:
            findings.append(Finding(
                title="Absolute Paths Detected",
                description="Replace absolute paths with relative paths.",
                severity=FindingSeverity.WARNING,
                category="reproducibility",
            ))

        return findings
