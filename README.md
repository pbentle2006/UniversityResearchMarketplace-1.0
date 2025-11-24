# University Research Marketplace

**Intelligent Research Lifecycle Orchestration**

A Streamlit prototype demonstrating how AI-powered Research Agents can address the academic reproducibility crisis while providing a comprehensive data marketplace experience.

## Features

### Six-Step Research Workflow

1. **Access Control** - Admin dashboard with system metrics and API monitoring
2. **Content Marketplace** - Browse and explore curated research datasets
3. **Search & Discovery** - AI-powered search with intelligent suggestions
4. **Curation** - Personalized recommendations based on research persona
5. **Insights** - AI-generated research questions and methodology recommendations
6. **Research Tools** - Integration with Jupyter, R Studio, Spark, and more

### Four Researcher Personas

- **Climate Researcher** - Environmental Science focus
- **Biomedical Researcher** - Life Sciences focus
- **Social Scientist** - Human Behavior focus
- **Data Scientist** - Analytics & ML focus

### AI Research Agents

- **Analysis Agent** - Statistical rigor and methodology validation
- **Integrity Agent** - Research ethics, data integrity, and compliance

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd UniversityResearchMarketplace-1.0
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## Project Structure

```
UniversityResearchMarketplace-1.0/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── PROJECT_PLAN.md          # Detailed project documentation
├── README.md                # This file
├── src/
│   ├── agents/              # AI Research Agents
│   │   ├── base_agent.py    # Base agent class
│   │   ├── analysis_agent.py # Statistical analysis agent
│   │   └── integrity_agent.py # Data integrity agent
│   ├── data/                # Mock data and constants
│   │   └── mock_data.py     # Sample datasets and personas
│   ├── models/              # Database models
│   │   └── database.py      # SQLAlchemy models
│   └── utils/               # Utility functions
├── data/                    # Database storage
└── tests/                   # Test files
```

## Usage

### Getting Started

1. Launch the application
2. Select your research persona on the onboarding screen
3. Navigate through the six-step workflow
4. Select datasets from the marketplace
5. Review AI-generated insights and recommendations
6. Launch research tools when ready

### Key Features

- **Persona-driven curation**: Recommendations tailored to your research field
- **AI agent analysis**: Automatic checks for statistical rigor and data integrity
- **Petabyte-scale metrics**: Demonstration of large-scale data management
- **Research tool integration**: Connect to Jupyter, R Studio, and more

## Development Roadmap

### Phase 1: Foundation (Current)
- Core marketplace with 6-step navigation
- Persona selection and recommendations
- Analysis and Integrity agents
- Admin dashboard

### Phase 2: Enhanced Intelligence
- Testing and Collaboration agents
- Advanced search and recommendations
- Interactive visualizations

### Phase 3: Full Lifecycle Orchestration
- Documentation and Training agents
- Pre-registration workflow
- External tool connections

### Phase 4: Advanced Features
- Institutional dashboards
- External service integrations
- Demo scenarios

## Contributing

This is a prototype for demonstration purposes. For questions or feedback, please open an issue.

## License

MIT License - See LICENSE file for details.

## Acknowledgments

This project addresses the research reproducibility crisis by combining:
- Persona-driven data curation
- AI-powered methodology validation
- Transparent audit trails
- Integrated research workflows

---

*University Research Marketplace v1.0*
*Intelligent Research Lifecycle Orchestration*
