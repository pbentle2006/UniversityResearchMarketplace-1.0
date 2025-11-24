"""Analysis Agent for statistical rigor and methodology validation."""

from typing import List, Dict, Any
import random

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class AnalysisAgent(BaseAgent):
    """
    Analysis Agent for statistical rigor and methodology validation.

    Capabilities:
    - Pre-registration validation and power analysis
    - Statistical test appropriateness checking
    - P-hacking detection and prevention
    - Effect size calculation and interpretation
    - Bayesian alternative analysis suggestions
    - Data distribution and assumption testing
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Analysis Agent"
        self.description = "Statistical rigor and methodology validation"
        self.capabilities = [
            "Pre-registration validation",
            "Power analysis",
            "Statistical test checking",
            "P-hacking detection",
            "Effect size calculation",
            "Assumption testing",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze research data for statistical rigor.

        Args:
            data: Dictionary containing:
                - sample_size: Number of samples
                - variables: List of variable names
                - hypotheses: List of hypotheses
                - planned_tests: List of planned statistical tests
                - alpha_level: Significance level
                - pre_registered: Whether study is pre-registered

        Returns:
            AgentResult with statistical analysis findings
        """
        findings = []
        recommendations = []
        score = 100.0

        # Extract data with defaults
        sample_size = data.get('sample_size', 0)
        variables = data.get('variables', [])
        hypotheses = data.get('hypotheses', [])
        planned_tests = data.get('planned_tests', [])
        alpha_level = data.get('alpha_level', 0.05)
        pre_registered = data.get('pre_registered', False)

        # Check pre-registration
        if not pre_registered:
            findings.append(Finding(
                title="No Pre-registration Detected",
                description="Study does not appear to be pre-registered. Pre-registration helps prevent HARKing and p-hacking.",
                severity=FindingSeverity.WARNING,
                category="methodology",
            ))
            score -= 10

        # Check sample size / power analysis
        if sample_size > 0:
            if sample_size < 30:
                findings.append(Finding(
                    title="Small Sample Size",
                    description=f"Sample size of {sample_size} may be insufficient for reliable statistical inference.",
                    severity=FindingSeverity.ERROR,
                    category="power",
                ))
                score -= 20
            elif sample_size < 100:
                findings.append(Finding(
                    title="Moderate Sample Size",
                    description=f"Sample size of {sample_size} is adequate for basic analyses but may limit detection of small effects.",
                    severity=FindingSeverity.WARNING,
                    category="power",
                ))
                score -= 5
            else:
                findings.append(Finding(
                    title="Adequate Sample Size",
                    description=f"Sample size of {sample_size} appears adequate for most statistical analyses.",
                    severity=FindingSeverity.SUCCESS,
                    category="power",
                ))

        # Check multiple comparisons
        num_tests = len(planned_tests) if planned_tests else len(hypotheses)
        if num_tests > 1:
            corrected_alpha = alpha_level / num_tests
            findings.append(Finding(
                title="Multiple Comparisons Detected",
                description=f"Planning {num_tests} statistical tests. Consider applying correction (e.g., Bonferroni: α = {corrected_alpha:.4f}).",
                severity=FindingSeverity.WARNING,
                category="methodology",
            ))
            score -= 5

        # Check for common p-hacking indicators
        if len(hypotheses) > 5:
            findings.append(Finding(
                title="Many Hypotheses",
                description=f"Testing {len(hypotheses)} hypotheses increases risk of false positives. Ensure primary hypotheses are clearly specified.",
                severity=FindingSeverity.WARNING,
                category="p-hacking",
            ))
            score -= 10

        # Persona-specific checks
        context = self.get_persona_context()

        if self.persona == "bio":
            findings.append(Finding(
                title="Population Stratification Check",
                description="For genomic studies, ensure population stratification is properly controlled.",
                severity=FindingSeverity.INFO,
                category="methodology",
            ))

        elif self.persona == "climate":
            findings.append(Finding(
                title="Temporal Autocorrelation",
                description="Climate data often exhibits temporal autocorrelation. Consider appropriate time series methods.",
                severity=FindingSeverity.INFO,
                category="methodology",
            ))

        elif self.persona == "social":
            findings.append(Finding(
                title="Effect Size Reporting",
                description="Social science research should report effect sizes alongside p-values for practical significance.",
                severity=FindingSeverity.INFO,
                category="reporting",
            ))

        elif self.persona == "data":
            findings.append(Finding(
                title="Cross-Validation Required",
                description="ML models should use proper cross-validation to avoid overfitting.",
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

        # Ensure score is within bounds
        score = max(0, min(100, score))

        return AgentResult(
            score=score,
            status=self._get_status(score),
            findings=findings,
            recommendations=recommendations,
            metadata={
                "sample_size": sample_size,
                "num_tests": num_tests,
                "pre_registered": pre_registered,
                "persona": self.persona,
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate recommendations based on analysis findings."""
        recommendations = []

        # Check for specific issues in findings
        for finding in analysis_result.findings:
            if finding.severity == FindingSeverity.ERROR:
                if "sample" in finding.title.lower():
                    recommendations.append(Recommendation(
                        title="Increase Sample Size",
                        description="Consider collecting more data or using power analysis to determine adequate sample size.",
                        priority=1,
                        action_items=[
                            "Conduct a priori power analysis using G*Power or similar tool",
                            "Consider effect size estimates from pilot studies or literature",
                            "If sample increase not possible, consider alternative analyses for small samples",
                        ],
                        resources=[
                            "G*Power software: https://www.psychologie.hhu.de/gpower",
                            "Cohen's effect size guidelines",
                        ],
                    ))

            if finding.severity == FindingSeverity.WARNING:
                if "pre-registration" in finding.title.lower():
                    recommendations.append(Recommendation(
                        title="Pre-register Your Study",
                        description="Pre-registration increases transparency and reduces risk of p-hacking.",
                        priority=2,
                        action_items=[
                            "Create pre-registration on OSF, AsPredicted, or domain-specific registry",
                            "Specify primary and secondary hypotheses",
                            "Document planned analyses and stopping rules",
                        ],
                        resources=[
                            "OSF Registries: https://osf.io/registries",
                            "AsPredicted: https://aspredicted.org",
                        ],
                    ))

                if "multiple" in finding.title.lower():
                    recommendations.append(Recommendation(
                        title="Apply Multiple Comparison Correction",
                        description="Control family-wise error rate when conducting multiple tests.",
                        priority=2,
                        action_items=[
                            "Apply Bonferroni, Holm, or FDR correction",
                            "Clearly distinguish confirmatory from exploratory analyses",
                            "Consider using hierarchical or Bayesian approaches",
                        ],
                        resources=[
                            "Benjamini-Hochberg FDR procedure",
                        ],
                    ))

        # Always recommend effect sizes
        recommendations.append(Recommendation(
            title="Report Effect Sizes",
            description="Include effect sizes with confidence intervals for all key findings.",
            priority=3,
            action_items=[
                "Calculate Cohen's d, η², r, or appropriate effect size measure",
                "Include 95% confidence intervals",
                "Interpret practical significance alongside statistical significance",
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

    def check_statistical_assumptions(self, data: Dict[str, Any]) -> List[Finding]:
        """
        Check common statistical assumptions.

        Args:
            data: Data to check assumptions for

        Returns:
            List of findings about assumption violations
        """
        findings = []

        # This would contain actual statistical tests in production
        # For the prototype, we return informational findings

        findings.append(Finding(
            title="Normality Assumption",
            description="Check normality using Shapiro-Wilk test or Q-Q plots before parametric tests.",
            severity=FindingSeverity.INFO,
            category="assumptions",
        ))

        findings.append(Finding(
            title="Homogeneity of Variance",
            description="Check variance equality using Levene's test for group comparisons.",
            severity=FindingSeverity.INFO,
            category="assumptions",
        ))

        findings.append(Finding(
            title="Independence",
            description="Ensure observations are independent; consider mixed models for nested data.",
            severity=FindingSeverity.INFO,
            category="assumptions",
        ))

        return findings
