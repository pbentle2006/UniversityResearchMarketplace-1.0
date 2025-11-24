"""Mock data for the Research Marketplace prototype."""

from datetime import datetime, timedelta
import random

# Dataset definitions matching the POC
MOCK_DATASETS = [
    {
        "id": "ds-001",
        "name": "Global Climate Research Database",
        "description": "Comprehensive climate data from 1950-2024 including temperature, precipitation, and atmospheric conditions across 10,000+ monitoring stations worldwide.",
        "provider": "NOAA",
        "format": "NetCDF, CSV, JSON",
        "size": "2.3 TB",
        "sample_count": 15000000,
        "tags": ["climate", "weather", "atmospheric", "temperature", "precipitation"],
        "access_type": "available",
        "relevance_scores": {"climate": 95, "bio": 40, "social": 25, "data": 70},
        "last_updated": "2024-12-15",
        "quality_score": 92,
    },
    {
        "id": "ds-002",
        "name": "Human Genome Variants Dataset",
        "description": "Large-scale genomic variation data across diverse populations including SNPs, indels, and structural variants from 100,000+ individuals.",
        "provider": "NIH/NCBI",
        "format": "VCF, FASTA, TSV",
        "size": "850 GB",
        "sample_count": 2500000,
        "tags": ["genomics", "genetics", "population", "variants", "DNA"],
        "access_type": "available",
        "relevance_scores": {"climate": 15, "bio": 95, "social": 30, "data": 75},
        "last_updated": "2024-11-20",
        "quality_score": 94,
    },
    {
        "id": "ds-003",
        "name": "Social Media Sentiment Archive",
        "description": "Anonymized social media posts with sentiment analysis from 2010-2024, including engagement metrics and temporal patterns.",
        "provider": "Stanford Digital Observatory",
        "format": "JSON, Parquet",
        "size": "1.7 TB",
        "sample_count": 50000000,
        "tags": ["social", "sentiment", "nlp", "behavior", "trends"],
        "access_type": "restricted",
        "relevance_scores": {"climate": 20, "bio": 25, "social": 95, "data": 85},
        "last_updated": "2024-12-01",
        "quality_score": 88,
    },
    {
        "id": "ds-004",
        "name": "Financial Markets Time Series",
        "description": "High-frequency trading data across global markets including equities, commodities, and forex with millisecond resolution.",
        "provider": "Bloomberg Research",
        "format": "HDF5, CSV",
        "size": "3.1 TB",
        "sample_count": 100000000,
        "tags": ["finance", "markets", "time-series", "trading", "economics"],
        "access_type": "available",
        "relevance_scores": {"climate": 30, "bio": 20, "social": 55, "data": 95},
        "last_updated": "2024-12-20",
        "quality_score": 90,
    },
    {
        "id": "ds-005",
        "name": "Medical Imaging Repository",
        "description": "Anonymized medical images with diagnostic labels including X-rays, CT scans, and MRIs across multiple pathologies.",
        "provider": "Mayo Clinic Research",
        "format": "DICOM, PNG, JSON",
        "size": "4.2 TB",
        "sample_count": 750000,
        "tags": ["medical", "imaging", "diagnostics", "radiology", "pathology"],
        "access_type": "restricted",
        "relevance_scores": {"climate": 10, "bio": 92, "social": 15, "data": 80},
        "last_updated": "2024-10-15",
        "quality_score": 96,
    },
    {
        "id": "ds-006",
        "name": "Ocean Temperature & Salinity Dataset",
        "description": "Global ocean measurements from Argo floats and research vessels, covering depth profiles and seasonal variations.",
        "provider": "Woods Hole Oceanographic",
        "format": "NetCDF, CSV",
        "size": "890 GB",
        "sample_count": 8500000,
        "tags": ["ocean", "climate", "temperature", "salinity", "marine"],
        "access_type": "available",
        "relevance_scores": {"climate": 92, "bio": 60, "social": 20, "data": 65},
        "last_updated": "2024-11-30",
        "quality_score": 91,
    },
    {
        "id": "ds-007",
        "name": "Public Health Survey Archive",
        "description": "Longitudinal health surveys from 50+ countries including demographics, health behaviors, and outcomes.",
        "provider": "WHO Research Division",
        "format": "SPSS, CSV, JSON",
        "size": "125 GB",
        "sample_count": 5000000,
        "tags": ["health", "survey", "demographics", "epidemiology", "public-health"],
        "access_type": "available",
        "relevance_scores": {"climate": 35, "bio": 85, "social": 88, "data": 70},
        "last_updated": "2024-09-15",
        "quality_score": 87,
    },
    {
        "id": "ds-008",
        "name": "Urban Mobility Patterns Dataset",
        "description": "Anonymized transportation and movement data from major metropolitan areas including traffic, transit, and pedestrian flows.",
        "provider": "MIT Senseable City Lab",
        "format": "Parquet, GeoJSON",
        "size": "2.1 TB",
        "sample_count": 30000000,
        "tags": ["urban", "mobility", "transportation", "geospatial", "smart-city"],
        "access_type": "restricted",
        "relevance_scores": {"climate": 55, "bio": 30, "social": 82, "data": 88},
        "last_updated": "2024-12-10",
        "quality_score": 85,
    },
]

# Persona definitions
PERSONAS = {
    "climate": {
        "id": "climate",
        "name": "Climate Researcher",
        "focus": "Environmental Science",
        "icon": "🌍",
        "color": "#2E7D32",
        "keywords": ["climate", "weather", "atmospheric", "ocean", "temperature"],
        "methods": ["Time series analysis", "Spatial modeling", "Trend detection", "Climate projections"],
        "tools": ["NetCDF tools", "Climate Data Operators", "Python xarray", "R ncdf4"],
    },
    "bio": {
        "id": "bio",
        "name": "Biomedical Researcher",
        "focus": "Life Sciences",
        "icon": "🧬",
        "color": "#1565C0",
        "keywords": ["genomics", "genetics", "medical", "health", "biology"],
        "methods": ["Statistical genetics", "Survival analysis", "Image classification", "GWAS"],
        "tools": ["Bioconductor", "PLINK", "PyTorch Medical", "FreeSurfer"],
    },
    "social": {
        "id": "social",
        "name": "Social Scientist",
        "focus": "Human Behavior",
        "icon": "👥",
        "color": "#7B1FA2",
        "keywords": ["social", "sentiment", "behavior", "survey", "demographics"],
        "methods": ["Sentiment analysis", "Network analysis", "Regression modeling", "Qualitative coding"],
        "tools": ["SPSS", "NVivo", "NetworkX", "NLTK"],
    },
    "data": {
        "id": "data",
        "name": "Data Scientist",
        "focus": "Analytics & ML",
        "icon": "📊",
        "color": "#E65100",
        "keywords": ["time-series", "analytics", "markets", "prediction", "machine-learning"],
        "methods": ["Machine learning", "Predictive modeling", "Deep learning", "Feature engineering"],
        "tools": ["TensorFlow", "PyTorch", "Spark MLlib", "scikit-learn"],
    },
}

# System metrics for admin dashboard
SYSTEM_METRICS = {
    "total_storage": "127.3 PB",
    "active_datasets": 15847,
    "daily_ingestion": "2.1 TB",
    "query_response": "<50ms avg",
    "active_users": 1247,
    "pending_requests": 23,
    "system_load": 67,
}

# Recent activity for admin dashboard
RECENT_ACTIVITY = [
    {"user": "Dr. Martinez", "action": "Accessed Climate Dataset", "time": "2 min ago", "status": "success"},
    {"user": "Research Team Alpha", "action": "Requested Genomic Data", "time": "15 min ago", "status": "pending"},
    {"user": "Prof. Johnson", "action": "Downloaded Financial Dataset", "time": "1 hour ago", "status": "success"},
    {"user": "Graduate Student", "action": "Search: social sentiment", "time": "2 hours ago", "status": "info"},
    {"user": "Dr. Chen", "action": "Ran Analysis Agent", "time": "3 hours ago", "status": "success"},
]

# API connectivity status
API_STATUS = [
    {"name": "NOAA Climate API", "status": "Connected", "latency": "45ms"},
    {"name": "NIH Genomics Portal", "status": "Connected", "latency": "78ms"},
    {"name": "Stanford Data Observatory", "status": "Connected", "latency": "92ms"},
    {"name": "Bloomberg Research API", "status": "Maintenance", "latency": "N/A"},
    {"name": "Mayo Clinic Repository", "status": "Connected", "latency": "156ms"},
]

# Research tools
RESEARCH_TOOLS = [
    {
        "name": "Jupyter Notebooks",
        "description": "Interactive computing environment for data analysis",
        "icon": "🔬",
        "status": "Available",
    },
    {
        "name": "R Studio Server",
        "description": "Statistical computing and graphics environment",
        "icon": "📊",
        "status": "Available",
    },
    {
        "name": "Apache Spark",
        "description": "Large-scale data processing and analytics",
        "icon": "⚡",
        "status": "Available",
    },
    {
        "name": "Tableau",
        "description": "Advanced data visualization and dashboard creation",
        "icon": "📈",
        "status": "Available",
    },
    {
        "name": "TensorFlow/PyTorch",
        "description": "Machine learning and deep learning frameworks",
        "icon": "🤖",
        "status": "Available",
    },
    {
        "name": "Git/Version Control",
        "description": "Research project version control and collaboration",
        "icon": "🔄",
        "status": "Available",
    },
]

# Search suggestions by domain
SEARCH_SUGGESTIONS = {
    "climate": ["global warming trends", "precipitation patterns", "temperature anomalies", "sea level rise"],
    "genome": ["genetic variants", "population genetics", "gene expression", "GWAS studies"],
    "social": ["sentiment analysis", "behavior patterns", "social networks", "public opinion"],
    "financial": ["market volatility", "trading patterns", "economic indicators", "risk modeling"],
}


def get_persona_research_questions(persona: str) -> list:
    """Get research questions specific to a persona."""
    questions = {
        "climate": [
            "How have temperature patterns shifted in the last decade?",
            "What correlation exists between precipitation and atmospheric conditions?",
            "Can we predict future climate anomalies based on historical data?",
            "What is the rate of ocean acidification across different regions?",
        ],
        "bio": [
            "What genetic variants show population-specific patterns?",
            "How do variant frequencies differ across demographic groups?",
            "Which genomic regions show the highest variation rates?",
            "Can we identify biomarkers for early disease detection?",
        ],
        "social": [
            "How has social sentiment evolved over time?",
            "What factors drive changes in public opinion?",
            "Can we identify early indicators of social trends?",
            "What network patterns predict information spread?",
        ],
        "data": [
            "What patterns emerge from high-frequency market data?",
            "How can machine learning improve prediction accuracy?",
            "What external factors influence market volatility?",
            "Can we detect anomalies in real-time data streams?",
        ],
    }
    return questions.get(persona, [])


def get_persona_methodology(persona: str) -> str:
    """Get methodology recommendations for a persona."""
    methodologies = {
        "climate": "climate trend analysis with statistical modeling and spatial interpolation techniques",
        "bio": "genomic variant analysis with population stratification and statistical genetics methods",
        "social": "sentiment analysis with behavioral pattern recognition and network analysis",
        "data": "time series analysis with machine learning prediction models and ensemble methods",
    }
    return methodologies.get(persona, "general statistical analysis")
