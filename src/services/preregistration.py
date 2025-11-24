"""Pre-registration workflow service for research studies."""

from typing import Dict, Any, List
from datetime import datetime
from enum import Enum


class PreregistrationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    AMENDED = "amended"


class PreregistrationTemplate:
    """Templates for different pre-registration types."""

    @staticmethod
    def get_osf_template() -> Dict[str, Any]:
        """Get OSF pre-registration template."""
        return {
            "name": "OSF Pre-registration",
            "sections": [
                {
                    "id": "study_info",
                    "title": "Study Information",
                    "fields": [
                        {"id": "title", "label": "Study Title", "type": "text", "required": True},
                        {"id": "authors", "label": "Authors", "type": "text", "required": True},
                        {"id": "description", "label": "Study Description", "type": "textarea", "required": True},
                    ],
                },
                {
                    "id": "hypotheses",
                    "title": "Hypotheses",
                    "fields": [
                        {"id": "hypotheses", "label": "Research Hypotheses", "type": "textarea", "required": True,
                         "help": "List your specific, testable hypotheses"},
                    ],
                },
                {
                    "id": "design",
                    "title": "Design Plan",
                    "fields": [
                        {"id": "study_type", "label": "Study Type", "type": "select", "required": True,
                         "options": ["Experiment", "Observational", "Meta-analysis", "Other"]},
                        {"id": "blinding", "label": "Blinding", "type": "select", "required": True,
                         "options": ["No blinding", "Single-blind", "Double-blind"]},
                        {"id": "design_details", "label": "Design Details", "type": "textarea", "required": True},
                    ],
                },
                {
                    "id": "sampling",
                    "title": "Sampling Plan",
                    "fields": [
                        {"id": "sample_size", "label": "Planned Sample Size", "type": "number", "required": True},
                        {"id": "sample_rationale", "label": "Sample Size Rationale", "type": "textarea", "required": True,
                         "help": "How did you determine sample size? Include power analysis if applicable"},
                        {"id": "stopping_rule", "label": "Stopping Rule", "type": "textarea", "required": False},
                    ],
                },
                {
                    "id": "variables",
                    "title": "Variables",
                    "fields": [
                        {"id": "ivs", "label": "Independent Variables", "type": "textarea", "required": True},
                        {"id": "dvs", "label": "Dependent Variables", "type": "textarea", "required": True},
                        {"id": "covariates", "label": "Covariates", "type": "textarea", "required": False},
                    ],
                },
                {
                    "id": "analysis",
                    "title": "Analysis Plan",
                    "fields": [
                        {"id": "statistical_models", "label": "Statistical Models", "type": "textarea", "required": True},
                        {"id": "transformations", "label": "Data Transformations", "type": "textarea", "required": False},
                        {"id": "inference_criteria", "label": "Inference Criteria", "type": "textarea", "required": True,
                         "help": "e.g., alpha level, correction for multiple comparisons"},
                        {"id": "exclusion_criteria", "label": "Data Exclusion Criteria", "type": "textarea", "required": True},
                        {"id": "missing_data", "label": "Missing Data Handling", "type": "textarea", "required": True},
                        {"id": "exploratory", "label": "Exploratory Analyses", "type": "textarea", "required": False},
                    ],
                },
            ],
        }

    @staticmethod
    def get_aspredicted_template() -> Dict[str, Any]:
        """Get AsPredicted template (simpler format)."""
        return {
            "name": "AsPredicted",
            "sections": [
                {
                    "id": "main",
                    "title": "Pre-registration",
                    "fields": [
                        {"id": "data_collection", "label": "Have any data been collected for this study already?",
                         "type": "select", "required": True,
                         "options": ["No", "Yes, part of the data", "Yes, all of the data"]},
                        {"id": "hypothesis", "label": "What's the main question being asked or hypothesis being tested?",
                         "type": "textarea", "required": True},
                        {"id": "dvs", "label": "Dependent variable(s)", "type": "textarea", "required": True},
                        {"id": "conditions", "label": "Conditions/Groups", "type": "textarea", "required": True},
                        {"id": "analyses", "label": "Analyses", "type": "textarea", "required": True},
                        {"id": "outliers", "label": "Outliers and exclusions", "type": "textarea", "required": True},
                        {"id": "sample_size", "label": "Sample size", "type": "textarea", "required": True},
                        {"id": "other", "label": "Other", "type": "textarea", "required": False},
                    ],
                },
            ],
        }


class PreregistrationService:
    """Service for managing pre-registration workflow."""

    def __init__(self):
        self.templates = {
            "osf": PreregistrationTemplate.get_osf_template(),
            "aspredicted": PreregistrationTemplate.get_aspredicted_template(),
        }

    def create_preregistration(self, template_id: str, user_id: str) -> Dict[str, Any]:
        """
        Create a new pre-registration draft.

        Args:
            template_id: ID of template to use
            user_id: User creating the pre-registration

        Returns:
            New pre-registration object
        """
        template = self.templates.get(template_id, self.templates["osf"])

        return {
            "id": f"prereg-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "template": template_id,
            "status": PreregistrationStatus.DRAFT.value,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "data": {},
            "sections": template["sections"],
        }

    def validate_preregistration(self, prereg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a pre-registration for completeness.

        Args:
            prereg: Pre-registration data

        Returns:
            Validation result with any issues
        """
        issues = []
        warnings = []

        data = prereg.get("data", {})
        sections = prereg.get("sections", [])

        for section in sections:
            for field in section.get("fields", []):
                field_id = field["id"]
                is_required = field.get("required", False)
                value = data.get(field_id, "")

                if is_required and not value:
                    issues.append({
                        "field": field_id,
                        "label": field["label"],
                        "issue": "Required field is empty",
                    })

        # Check for common issues
        if "sample_size" in data:
            try:
                size = int(data["sample_size"])
                if size < 10:
                    warnings.append({
                        "field": "sample_size",
                        "warning": "Very small sample size. Ensure this is intentional.",
                    })
            except (ValueError, TypeError):
                pass

        if "hypotheses" in data or "hypothesis" in data:
            hyp = data.get("hypotheses", data.get("hypothesis", ""))
            if hyp and len(hyp) < 50:
                warnings.append({
                    "field": "hypotheses",
                    "warning": "Hypothesis seems brief. Consider adding more detail.",
                })

        is_valid = len(issues) == 0

        return {
            "valid": is_valid,
            "issues": issues,
            "warnings": warnings,
            "completion": self._calculate_completion(prereg),
        }

    def _calculate_completion(self, prereg: Dict[str, Any]) -> float:
        """Calculate completion percentage."""
        data = prereg.get("data", {})
        sections = prereg.get("sections", [])

        total_fields = 0
        completed_fields = 0

        for section in sections:
            for field in section.get("fields", []):
                total_fields += 1
                if data.get(field["id"]):
                    completed_fields += 1

        return (completed_fields / total_fields * 100) if total_fields > 0 else 0

    def get_deviation_tracker(self, prereg_id: str) -> Dict[str, Any]:
        """
        Get deviation tracking information for a pre-registration.

        Args:
            prereg_id: Pre-registration ID

        Returns:
            Deviation tracking data
        """
        # Mock deviation tracker for prototype
        return {
            "prereg_id": prereg_id,
            "deviations": [],
            "has_deviations": False,
            "deviation_report_template": """
## Deviations from Pre-registration

### Deviation 1
- **Section**: [Section name]
- **Original Plan**: [What was pre-registered]
- **Actual**: [What was actually done]
- **Reason**: [Why the deviation occurred]
- **Impact**: [How this might affect results]
""",
        }

    def suggest_registry(self, persona: str, study_type: str) -> List[Dict[str, Any]]:
        """
        Suggest appropriate pre-registration registry based on study.

        Args:
            persona: Researcher persona
            study_type: Type of study

        Returns:
            List of recommended registries
        """
        registries = [
            {
                "name": "OSF Registries",
                "url": "https://osf.io/registries",
                "description": "General purpose, supports many templates",
                "recommended_for": ["all"],
            },
            {
                "name": "AsPredicted",
                "url": "https://aspredicted.org",
                "description": "Simple 8-question format",
                "recommended_for": ["social", "data"],
            },
            {
                "name": "ClinicalTrials.gov",
                "url": "https://clinicaltrials.gov",
                "description": "Required for clinical trials",
                "recommended_for": ["bio"],
            },
            {
                "name": "PROSPERO",
                "url": "https://www.crd.york.ac.uk/prospero/",
                "description": "For systematic reviews",
                "recommended_for": ["bio", "social"],
            },
        ]

        # Filter and rank by relevance
        recommended = []
        for registry in registries:
            if "all" in registry["recommended_for"] or persona in registry["recommended_for"]:
                recommended.append(registry)

        return recommended


# Pre-registration workflow steps
PREREG_WORKFLOW_STEPS = [
    {
        "step": 1,
        "name": "Choose Template",
        "description": "Select a pre-registration template that fits your study type",
    },
    {
        "step": 2,
        "name": "Study Information",
        "description": "Enter basic study information and hypotheses",
    },
    {
        "step": 3,
        "name": "Design & Sampling",
        "description": "Describe your study design and sampling plan",
    },
    {
        "step": 4,
        "name": "Variables & Analysis",
        "description": "Specify variables and analysis plan",
    },
    {
        "step": 5,
        "name": "Review & Submit",
        "description": "Review your pre-registration and submit to registry",
    },
]
