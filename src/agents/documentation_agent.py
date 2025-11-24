"""Documentation Agent for comprehensive research documentation and transparency."""

from typing import List, Dict, Any
from datetime import datetime

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class DocumentationAgent(BaseAgent):
    """
    Documentation Agent for comprehensive research documentation and transparency.

    Capabilities:
    - Automated methods section generation
    - Protocol documentation with sufficient detail
    - Data dictionary and codebook creation
    - Dependency and environment capture
    - FAIR principles compliance checking
    - Open science badge recommendations
    - Preprint and publication pathway guidance
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Documentation Agent"
        self.description = "Comprehensive research documentation and transparency"
        self.capabilities = [
            "Methods section generation",
            "Protocol documentation",
            "Data dictionary creation",
            "Environment capture",
            "FAIR compliance checking",
            "Open science badges",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze documentation completeness and quality.

        Args:
            data: Dictionary containing:
                - has_readme: Boolean
                - has_methods: Boolean
                - has_data_dictionary: Boolean
                - has_codebook: Boolean
                - has_license: Boolean
                - documentation_format: str (markdown, latex, etc.)
                - has_api_docs: Boolean
                - code_comments_ratio: float

        Returns:
            AgentResult with documentation analysis
        """
        findings = []
        score = 100.0

        # Extract data
        has_readme = data.get('has_readme', False)
        has_methods = data.get('has_methods', False)
        has_data_dict = data.get('has_data_dictionary', False)
        has_codebook = data.get('has_codebook', False)
        has_license = data.get('has_license', False)
        doc_format = data.get('documentation_format', 'none')
        has_api_docs = data.get('has_api_docs', False)
        comment_ratio = data.get('code_comments_ratio', 0.0)

        # Check README
        if has_readme:
            findings.append(Finding(
                title="README Present",
                description="Project includes README with basic documentation.",
                severity=FindingSeverity.SUCCESS,
                category="documentation",
            ))
        else:
            findings.append(Finding(
                title="No README",
                description="Add a README file to describe your project.",
                severity=FindingSeverity.ERROR,
                category="documentation",
            ))
            score -= 20

        # Check methods documentation
        if has_methods:
            findings.append(Finding(
                title="Methods Documented",
                description="Research methods are documented.",
                severity=FindingSeverity.SUCCESS,
                category="methods",
            ))
        else:
            findings.append(Finding(
                title="Methods Not Documented",
                description="Document your methods with sufficient detail for replication.",
                severity=FindingSeverity.WARNING,
                category="methods",
            ))
            score -= 15

        # Check data dictionary
        if has_data_dict:
            findings.append(Finding(
                title="Data Dictionary Present",
                description="Variables and data structures are documented.",
                severity=FindingSeverity.SUCCESS,
                category="data",
            ))
        else:
            findings.append(Finding(
                title="No Data Dictionary",
                description="Create a data dictionary describing all variables.",
                severity=FindingSeverity.WARNING,
                category="data",
            ))
            score -= 10

        # Check codebook
        if has_codebook:
            findings.append(Finding(
                title="Codebook Present",
                description="Coding schemes and categories are documented.",
                severity=FindingSeverity.SUCCESS,
                category="data",
            ))

        # Check license
        if has_license:
            findings.append(Finding(
                title="License Specified",
                description="Project has a clear license for reuse.",
                severity=FindingSeverity.SUCCESS,
                category="legal",
            ))
        else:
            findings.append(Finding(
                title="No License",
                description="Add a license to clarify usage rights.",
                severity=FindingSeverity.WARNING,
                category="legal",
            ))
            score -= 5

        # Check code comments
        if comment_ratio >= 0.15:
            findings.append(Finding(
                title="Good Code Documentation",
                description=f"Code comment ratio of {comment_ratio:.0%} is adequate.",
                severity=FindingSeverity.SUCCESS,
                category="code",
            ))
        elif comment_ratio >= 0.05:
            findings.append(Finding(
                title="Moderate Code Documentation",
                description=f"Code comment ratio of {comment_ratio:.0%} could be improved.",
                severity=FindingSeverity.INFO,
                category="code",
            ))
        else:
            findings.append(Finding(
                title="Low Code Documentation",
                description="Add more comments to explain complex logic.",
                severity=FindingSeverity.WARNING,
                category="code",
            ))
            score -= 10

        # Check FAIR principles
        fair_score = self._calculate_fair_score(data)
        if fair_score >= 80:
            findings.append(Finding(
                title="FAIR Compliant",
                description=f"Documentation meets FAIR principles ({fair_score:.0f}%).",
                severity=FindingSeverity.SUCCESS,
                category="fair",
            ))
        elif fair_score >= 50:
            findings.append(Finding(
                title="Partial FAIR Compliance",
                description=f"FAIR score of {fair_score:.0f}%. Improve findability and accessibility.",
                severity=FindingSeverity.WARNING,
                category="fair",
            ))
            score -= 10
        else:
            findings.append(Finding(
                title="Low FAIR Compliance",
                description=f"FAIR score of {fair_score:.0f}%. Review FAIR principles.",
                severity=FindingSeverity.ERROR,
                category="fair",
            ))
            score -= 20

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
                "has_readme": has_readme,
                "has_methods": has_methods,
                "has_data_dict": has_data_dict,
                "fair_score": fair_score,
                "comment_ratio": comment_ratio,
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate recommendations for documentation improvement."""
        recommendations = []

        for finding in analysis_result.findings:
            if "readme" in finding.title.lower() and finding.severity == FindingSeverity.ERROR:
                recommendations.append(Recommendation(
                    title="Create Comprehensive README",
                    description="Add a README with project overview, installation, and usage instructions.",
                    priority=1,
                    action_items=[
                        "Add project title and description",
                        "Include installation instructions",
                        "Provide usage examples",
                        "List dependencies and requirements",
                        "Add citation information",
                    ],
                    resources=[
                        "README template: makeareadme.com",
                    ],
                ))

            if "data dictionary" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Create Data Dictionary",
                    description="Document all variables with names, types, and descriptions.",
                    priority=2,
                    action_items=[
                        "List all variable names",
                        "Specify data types",
                        "Provide descriptions and units",
                        "Document missing value codes",
                        "Include value ranges or categories",
                    ],
                    resources=[],
                ))

            if "fair" in finding.title.lower() and finding.severity != FindingSeverity.SUCCESS:
                recommendations.append(Recommendation(
                    title="Improve FAIR Compliance",
                    description="Enhance Findability, Accessibility, Interoperability, and Reusability.",
                    priority=2,
                    action_items=[
                        "Add persistent identifier (DOI)",
                        "Use standard metadata schemas",
                        "Choose open file formats",
                        "Add clear license",
                        "Provide rich documentation",
                    ],
                    resources=[
                        "FAIR principles: go-fair.org",
                    ],
                ))

        # Always recommend version documentation
        recommendations.append(Recommendation(
            title="Document Software Versions",
            description="Record all software and package versions used.",
            priority=3,
            action_items=[
                "Create requirements.txt or environment.yml",
                "Document R sessionInfo() or Python sys.version",
                "Note operating system version",
                "Record hardware specifications if relevant",
            ],
            resources=[],
        ))

        return recommendations

    def _calculate_fair_score(self, data: Dict[str, Any]) -> float:
        """Calculate FAIR principles compliance score."""
        score = 0
        max_score = 100

        # Findable (25 points)
        if data.get('has_persistent_id', False):
            score += 15
        if data.get('has_metadata', False):
            score += 10

        # Accessible (25 points)
        if data.get('has_access_protocol', False):
            score += 15
        if data.get('has_readme', False):
            score += 10

        # Interoperable (25 points)
        if data.get('uses_standard_formats', False):
            score += 15
        if data.get('has_data_dictionary', False):
            score += 10

        # Reusable (25 points)
        if data.get('has_license', False):
            score += 15
        if data.get('has_methods', False):
            score += 10

        return (score / max_score) * 100

    def _get_status(self, score: float) -> str:
        """Get status string based on score."""
        if score >= 80:
            return "pass"
        elif score >= 60:
            return "warn"
        else:
            return "fail"

    def generate_methods_section(self, project_data: Dict[str, Any]) -> str:
        """
        Generate a draft methods section based on project data.

        Args:
            project_data: Project information

        Returns:
            Draft methods section text
        """
        persona = self.persona or "data"

        templates = {
            "climate": """
## Methods

### Data Sources
Data were obtained from [specify sources]. The dataset spans [time period] and includes [variables].

### Data Processing
Raw data were processed using [software/version]. Quality control procedures included [list procedures].

### Statistical Analysis
[Describe analytical approach]. All analyses were conducted using [software] version [X.X].

### Code Availability
Analysis code is available at [repository URL].
""",
            "bio": """
## Methods

### Study Design
[Describe study type: cohort, case-control, etc.]

### Participants/Samples
[Describe sample size, selection criteria, demographics]

### Data Collection
[Describe data collection procedures]

### Statistical Analysis
Statistical analyses were performed using [software]. [Describe tests used]. P-values < 0.05 were considered statistically significant.

### Ethics
This study was approved by [IRB/Ethics committee] (Protocol #XXX).
""",
            "social": """
## Methods

### Participants
[N] participants were recruited from [source]. Inclusion criteria were [list].

### Measures
[List and describe all measures with reliability information]

### Procedure
[Describe study procedure]

### Analysis
Data were analyzed using [software]. [Describe analytical approach].

### Pre-registration
This study was pre-registered at [URL].
""",
            "data": """
## Methods

### Data
[Describe data source, size, and features]

### Preprocessing
Data preprocessing included [list steps]. Missing values were handled by [method].

### Model
[Describe model architecture/algorithm]

### Training
Models were trained using [framework]. Hyperparameters were tuned using [method].

### Evaluation
Model performance was evaluated using [metrics] with [cross-validation strategy].

### Reproducibility
Code and trained models are available at [URL]. Random seeds were set for reproducibility.
""",
        }

        return templates.get(persona, templates["data"])

    def suggest_open_science_badges(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest applicable open science badges based on project.

        Args:
            data: Project data

        Returns:
            List of suggested badges with requirements
        """
        badges = []

        if data.get('has_open_data', False):
            badges.append({
                "name": "Open Data",
                "icon": "📊",
                "status": "Eligible",
                "requirements": "Data publicly available with documentation",
            })
        else:
            badges.append({
                "name": "Open Data",
                "icon": "📊",
                "status": "Not Yet",
                "requirements": "Make data publicly available with documentation",
            })

        if data.get('has_open_materials', False):
            badges.append({
                "name": "Open Materials",
                "icon": "📦",
                "status": "Eligible",
                "requirements": "Materials publicly available",
            })

        if data.get('is_preregistered', False):
            badges.append({
                "name": "Preregistered",
                "icon": "📝",
                "status": "Eligible",
                "requirements": "Study preregistered before data collection",
            })

        return badges
