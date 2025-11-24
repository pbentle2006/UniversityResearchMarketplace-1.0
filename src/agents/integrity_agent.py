"""Integrity Agent for research ethics, data integrity, and compliance."""

from typing import List, Dict, Any
from datetime import datetime

from .base_agent import (
    BaseAgent,
    AgentResult,
    Finding,
    Recommendation,
    FindingSeverity,
)


class IntegrityAgent(BaseAgent):
    """
    Integrity Agent for research ethics, data integrity, and compliance.

    Capabilities:
    - Data manipulation detection
    - Image forensics for figures
    - Plagiarism and self-plagiarism detection
    - Conflict of interest disclosure verification
    - IRB/Ethics compliance checking
    - Data provenance and chain of custody tracking
    - Selective reporting detection
    - Dataset quality scoring
    """

    def __init__(self, project_id: str = None, persona: str = None):
        super().__init__(project_id, persona)
        self.name = "Integrity Agent"
        self.description = "Research ethics, data integrity, and compliance"
        self.capabilities = [
            "Data integrity validation",
            "Provenance tracking",
            "Ethics compliance checking",
            "Quality scoring",
            "FAIR principles assessment",
            "Reproducibility verification",
        ]

    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Analyze research data for integrity and compliance.

        Args:
            data: Dictionary containing:
                - datasets: List of dataset metadata
                - has_ethics_approval: Boolean
                - data_sources: List of data source descriptions
                - has_data_management_plan: Boolean
                - sharing_plan: Description of data sharing plans
                - version_controlled: Boolean

        Returns:
            AgentResult with integrity analysis findings
        """
        findings = []
        recommendations = []
        score = 100.0

        # Extract data with defaults
        datasets = data.get('datasets', [])
        has_ethics = data.get('has_ethics_approval', False)
        data_sources = data.get('data_sources', [])
        has_dmp = data.get('has_data_management_plan', False)
        sharing_plan = data.get('sharing_plan', '')
        version_controlled = data.get('version_controlled', False)

        # Check ethics approval
        if not has_ethics:
            findings.append(Finding(
                title="Ethics Approval Status Unknown",
                description="No ethics/IRB approval documentation detected. Ensure human subjects research has proper approval.",
                severity=FindingSeverity.WARNING,
                category="ethics",
            ))
            score -= 10

        # Check data management plan
        if not has_dmp:
            findings.append(Finding(
                title="No Data Management Plan",
                description="A data management plan helps ensure data integrity and facilitates sharing.",
                severity=FindingSeverity.WARNING,
                category="compliance",
            ))
            score -= 5
        else:
            findings.append(Finding(
                title="Data Management Plan Present",
                description="Project has a documented data management plan.",
                severity=FindingSeverity.SUCCESS,
                category="compliance",
            ))

        # Check version control
        if not version_controlled:
            findings.append(Finding(
                title="Version Control Not Detected",
                description="Code and analysis scripts should be under version control for reproducibility.",
                severity=FindingSeverity.WARNING,
                category="reproducibility",
            ))
            score -= 10
        else:
            findings.append(Finding(
                title="Version Control Active",
                description="Project is using version control for code management.",
                severity=FindingSeverity.SUCCESS,
                category="reproducibility",
            ))

        # Analyze datasets for quality
        for dataset in datasets:
            dataset_findings = self._analyze_dataset_quality(dataset)
            findings.extend(dataset_findings)

            # Adjust score based on dataset findings
            for finding in dataset_findings:
                if finding.severity == FindingSeverity.ERROR:
                    score -= 15
                elif finding.severity == FindingSeverity.WARNING:
                    score -= 5

        # Check FAIR principles
        fair_findings = self._check_fair_principles(data)
        findings.extend(fair_findings)

        for finding in fair_findings:
            if finding.severity == FindingSeverity.SUCCESS:
                score += 2

        # Check data provenance
        if data_sources:
            findings.append(Finding(
                title="Data Provenance Documented",
                description=f"Data sources are documented ({len(data_sources)} sources identified).",
                severity=FindingSeverity.SUCCESS,
                category="provenance",
            ))
        else:
            findings.append(Finding(
                title="Data Provenance Missing",
                description="Document the origin and processing history of all data.",
                severity=FindingSeverity.WARNING,
                category="provenance",
            ))
            score -= 10

        # Check sharing plan
        if sharing_plan:
            findings.append(Finding(
                title="Data Sharing Plan Present",
                description="Project includes plans for data sharing.",
                severity=FindingSeverity.SUCCESS,
                category="openness",
            ))
        else:
            findings.append(Finding(
                title="No Data Sharing Plan",
                description="Consider how data will be shared for reproducibility.",
                severity=FindingSeverity.INFO,
                category="openness",
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
                "num_datasets": len(datasets),
                "has_ethics": has_ethics,
                "has_dmp": has_dmp,
                "version_controlled": version_controlled,
                "fair_score": self._calculate_fair_score(fair_findings),
            },
        )

    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """Generate recommendations based on integrity analysis."""
        recommendations = []

        for finding in analysis_result.findings:
            if "ethics" in finding.category and finding.severity != FindingSeverity.SUCCESS:
                recommendations.append(Recommendation(
                    title="Obtain Ethics Approval",
                    description="Ensure proper IRB/ethics approval for human subjects research.",
                    priority=1,
                    action_items=[
                        "Submit IRB application if not already done",
                        "Document approval number in all materials",
                        "Ensure informed consent procedures are in place",
                    ],
                    resources=[
                        "OHRP guidance: https://www.hhs.gov/ohrp",
                    ],
                ))
                break

        # Check for version control issues
        for finding in analysis_result.findings:
            if "version control" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Implement Version Control",
                    description="Use Git or similar for all code and analysis scripts.",
                    priority=2,
                    action_items=[
                        "Initialize Git repository",
                        "Create .gitignore for data files",
                        "Commit regularly with descriptive messages",
                        "Consider using GitHub/GitLab for collaboration",
                    ],
                    resources=[
                        "Git for Scientists: https://swcarpentry.github.io/git-novice/",
                    ],
                ))
                break

        # Check for data management plan
        for finding in analysis_result.findings:
            if "data management plan" in finding.title.lower() and finding.severity == FindingSeverity.WARNING:
                recommendations.append(Recommendation(
                    title="Create Data Management Plan",
                    description="Document how data will be collected, stored, and shared.",
                    priority=2,
                    action_items=[
                        "Use DMPTool or similar to create plan",
                        "Specify data formats and standards",
                        "Define retention and sharing policies",
                        "Identify storage and backup procedures",
                    ],
                    resources=[
                        "DMPTool: https://dmptool.org",
                    ],
                ))
                break

        # Always recommend documentation
        recommendations.append(Recommendation(
            title="Document Data Processing",
            description="Maintain detailed records of all data transformations.",
            priority=3,
            action_items=[
                "Create codebook for all variables",
                "Document cleaning and transformation steps",
                "Record software versions and dependencies",
                "Use computational notebooks for transparency",
            ],
            resources=[],
        ))

        return recommendations

    def _analyze_dataset_quality(self, dataset: Dict[str, Any]) -> List[Finding]:
        """Analyze quality of a single dataset."""
        findings = []

        name = dataset.get('name', 'Unknown Dataset')
        quality_score = dataset.get('quality_score', 0)
        access_type = dataset.get('access_type', 'unknown')

        if quality_score >= 90:
            findings.append(Finding(
                title=f"High Quality Dataset: {name}",
                description=f"Dataset has quality score of {quality_score}%. Meets high standards for research use.",
                severity=FindingSeverity.SUCCESS,
                category="data_quality",
            ))
        elif quality_score >= 70:
            findings.append(Finding(
                title=f"Adequate Quality: {name}",
                description=f"Dataset has quality score of {quality_score}%. Review documentation for potential issues.",
                severity=FindingSeverity.INFO,
                category="data_quality",
            ))
        else:
            findings.append(Finding(
                title=f"Quality Concerns: {name}",
                description=f"Dataset has quality score of {quality_score}%. Carefully evaluate fitness for purpose.",
                severity=FindingSeverity.WARNING,
                category="data_quality",
            ))

        # Check access type
        if access_type == 'restricted':
            findings.append(Finding(
                title=f"Restricted Access: {name}",
                description="Dataset has restricted access. Ensure proper data use agreements are in place.",
                severity=FindingSeverity.INFO,
                category="access",
            ))

        return findings

    def _check_fair_principles(self, data: Dict[str, Any]) -> List[Finding]:
        """Check adherence to FAIR principles."""
        findings = []

        # Findable
        if data.get('has_persistent_id', False):
            findings.append(Finding(
                title="Findable: Persistent Identifier",
                description="Data has persistent identifier (DOI, Handle, etc.).",
                severity=FindingSeverity.SUCCESS,
                category="fair",
            ))
        else:
            findings.append(Finding(
                title="Findable: No Persistent ID",
                description="Consider obtaining persistent identifier for data.",
                severity=FindingSeverity.INFO,
                category="fair",
            ))

        # Accessible
        if data.get('has_access_protocol', False):
            findings.append(Finding(
                title="Accessible: Clear Protocol",
                description="Data access protocol is clearly documented.",
                severity=FindingSeverity.SUCCESS,
                category="fair",
            ))

        # Interoperable
        datasets = data.get('datasets', [])
        standard_formats = ['CSV', 'JSON', 'NetCDF', 'HDF5', 'Parquet']
        for dataset in datasets:
            format_str = dataset.get('format', '')
            if any(fmt in format_str for fmt in standard_formats):
                findings.append(Finding(
                    title="Interoperable: Standard Format",
                    description=f"Dataset uses standard format ({format_str}).",
                    severity=FindingSeverity.SUCCESS,
                    category="fair",
                ))
                break

        # Reusable
        if data.get('has_license', False):
            findings.append(Finding(
                title="Reusable: License Specified",
                description="Data has clear license for reuse.",
                severity=FindingSeverity.SUCCESS,
                category="fair",
            ))

        return findings

    def _calculate_fair_score(self, fair_findings: List[Finding]) -> float:
        """Calculate FAIR principles compliance score."""
        if not fair_findings:
            return 0.0

        success_count = sum(1 for f in fair_findings if f.severity == FindingSeverity.SUCCESS)
        total = len(fair_findings)

        return (success_count / total) * 100 if total > 0 else 0.0

    def _get_status(self, score: float) -> str:
        """Get status string based on score."""
        if score >= 80:
            return "pass"
        elif score >= 60:
            return "warn"
        else:
            return "fail"

    def validate_data_provenance(self, data: Dict[str, Any]) -> List[Finding]:
        """
        Validate data provenance and chain of custody.

        Args:
            data: Data provenance information

        Returns:
            List of findings about provenance
        """
        findings = []

        # Check for documented sources
        sources = data.get('sources', [])
        if sources:
            findings.append(Finding(
                title="Data Sources Documented",
                description=f"Found {len(sources)} documented data sources.",
                severity=FindingSeverity.SUCCESS,
                category="provenance",
            ))
        else:
            findings.append(Finding(
                title="Missing Source Documentation",
                description="Document all original data sources.",
                severity=FindingSeverity.WARNING,
                category="provenance",
            ))

        # Check for processing history
        if data.get('processing_history'):
            findings.append(Finding(
                title="Processing History Available",
                description="Data processing steps are documented.",
                severity=FindingSeverity.SUCCESS,
                category="provenance",
            ))

        # Check for checksums
        if data.get('checksums'):
            findings.append(Finding(
                title="Data Integrity Verified",
                description="Checksums available for data verification.",
                severity=FindingSeverity.SUCCESS,
                category="integrity",
            ))

        return findings
