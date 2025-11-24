"""Base class for all Research Agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class FindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class Finding:
    """A finding from an agent analysis."""
    title: str
    description: str
    severity: FindingSeverity
    category: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class Recommendation:
    """A recommendation from an agent."""
    title: str
    description: str
    priority: int  # 1-5, 1 being highest
    action_items: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)


@dataclass
class AgentResult:
    """Result from an agent analysis."""
    score: float  # 0-100
    status: str  # pass/warn/fail
    findings: List[Finding]
    recommendations: List[Recommendation]
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """Base class for all research agents."""

    def __init__(self, project_id: str = None, persona: str = None):
        self.project_id = project_id
        self.persona = persona
        self.name: str = "Base Agent"
        self.description: str = "Base agent class"
        self.capabilities: List[str] = []
        self.version: str = "1.0.0"

    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> AgentResult:
        """
        Main analysis method.

        Args:
            data: Input data for analysis

        Returns:
            AgentResult with score, findings, and recommendations
        """
        pass

    @abstractmethod
    def get_recommendations(self, analysis_result: AgentResult) -> List[Recommendation]:
        """
        Generate actionable recommendations based on analysis.

        Args:
            analysis_result: Result from analyze method

        Returns:
            List of recommendations
        """
        pass

    def get_persona_context(self) -> Dict[str, Any]:
        """
        Get persona-specific context and guidance.

        Returns:
            Dictionary with persona-specific information
        """
        persona_contexts = {
            "climate": {
                "focus_areas": ["temporal patterns", "spatial distributions", "trend analysis"],
                "common_issues": ["missing data handling", "seasonal adjustments", "outlier detection"],
                "recommended_tests": ["Mann-Kendall test", "Spatial autocorrelation", "Time series decomposition"],
            },
            "bio": {
                "focus_areas": ["population stratification", "multiple testing correction", "effect sizes"],
                "common_issues": ["batch effects", "confounding variables", "sample size adequacy"],
                "recommended_tests": ["Bonferroni correction", "FDR control", "Power analysis"],
            },
            "social": {
                "focus_areas": ["sampling bias", "response rates", "construct validity"],
                "common_issues": ["self-selection bias", "social desirability", "measurement error"],
                "recommended_tests": ["Cronbach's alpha", "Factor analysis", "ICC"],
            },
            "data": {
                "focus_areas": ["feature engineering", "model validation", "cross-validation"],
                "common_issues": ["data leakage", "overfitting", "class imbalance"],
                "recommended_tests": ["K-fold CV", "Feature importance", "Learning curves"],
            },
        }

        return persona_contexts.get(self.persona, {
            "focus_areas": ["general statistical analysis"],
            "common_issues": ["sample size", "assumption violations"],
            "recommended_tests": ["Descriptive statistics", "Normality tests"],
        })

    def generate_report(self, result: AgentResult) -> Dict[str, Any]:
        """
        Generate a detailed report from the analysis result.

        Args:
            result: AgentResult from analysis

        Returns:
            Dictionary containing formatted report
        """
        return {
            "agent_name": self.name,
            "agent_version": self.version,
            "timestamp": result.timestamp.isoformat(),
            "overall_score": result.score,
            "status": result.status,
            "findings_summary": {
                "total": len(result.findings),
                "by_severity": {
                    severity.value: len([f for f in result.findings if f.severity == severity])
                    for severity in FindingSeverity
                },
            },
            "recommendations_summary": {
                "total": len(result.recommendations),
                "high_priority": len([r for r in result.recommendations if r.priority <= 2]),
            },
            "findings": [
                {
                    "title": f.title,
                    "description": f.description,
                    "severity": f.severity.value,
                    "category": f.category,
                }
                for f in result.findings
            ],
            "recommendations": [
                {
                    "title": r.title,
                    "description": r.description,
                    "priority": r.priority,
                    "action_items": r.action_items,
                }
                for r in result.recommendations
            ],
            "metadata": result.metadata,
        }
