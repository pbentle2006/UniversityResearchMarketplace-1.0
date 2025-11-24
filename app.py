"""
University Research Marketplace - Intelligent Research Lifecycle Orchestration
A Streamlit prototype demonstrating AI-powered Research Agents for reproducibility.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data.mock_data import (
    MOCK_DATASETS,
    PERSONAS,
    SYSTEM_METRICS,
    RECENT_ACTIVITY,
    API_STATUS,
    RESEARCH_TOOLS,
    SEARCH_SUGGESTIONS,
    get_persona_research_questions,
    get_persona_methodology,
)

# Page configuration
st.set_page_config(
    page_title="Research Data Marketplace",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .dataset-card {
        border: 2px solid #E5E7EB;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .dataset-card:hover {
        border-color: #6366F1;
        background-color: #F5F3FF;
    }
    .tag {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        margin-right: 0.25rem;
        margin-bottom: 0.25rem;
    }
    .persona-card {
        border: 2px solid #E5E7EB;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    .persona-card:hover {
        border-color: #6366F1;
        background-color: #F5F3FF;
    }

    /* Standardized step navigation buttons */
    .step-nav-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        padding: 1rem 0;
        background: #F9FAFB;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
    }
    .step-nav-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-width: 120px;
        height: 70px;
        padding: 0.75rem 1rem;
        border: 2px solid #E5E7EB;
        border-radius: 0.5rem;
        background: white;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }
    .step-nav-btn:hover {
        border-color: #6366F1;
        background: #F5F3FF;
    }
    .step-nav-btn.active {
        border-color: #6366F1;
        background: #EEF2FF;
    }
    .step-nav-btn.completed {
        border-color: #10B981;
        background: #ECFDF5;
    }
    .step-nav-icon {
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    .step-nav-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: #374151;
        text-align: center;
        white-space: nowrap;
    }
    .step-nav-btn.active .step-nav-label {
        color: #4338CA;
        font-weight: 600;
    }
    .step-nav-btn.completed .step-nav-label {
        color: #059669;
    }

    .step-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin-right: 0.5rem;
        font-size: 0.875rem;
    }
    .step-active {
        background-color: #EEF2FF;
        color: #4338CA;
        font-weight: 600;
    }
    .step-completed {
        background-color: #DCFCE7;
        color: #166534;
    }
    .step-pending {
        color: #6B7280;
    }
    .insight-box {
        border-left: 4px solid;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .insight-blue {
        border-color: #3B82F6;
        background-color: #EFF6FF;
    }
    .insight-green {
        border-color: #10B981;
        background-color: #ECFDF5;
    }
    .insight-purple {
        border-color: #8B5CF6;
        background-color: #F5F3FF;
    }

    /* Ensure consistent button sizing in columns */
    div[data-testid="column"] > div > div > div > button {
        min-height: 70px !important;
        white-space: nowrap !important;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0  # 0 = onboarding
    if 'user_persona' not in st.session_state:
        st.session_state.user_persona = None
    if 'selected_datasets' not in st.session_state:
        st.session_state.selected_datasets = []
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'show_onboarding' not in st.session_state:
        st.session_state.show_onboarding = True


def render_onboarding():
    """Render the persona selection onboarding screen."""
    st.markdown('<p class="main-header">Research Data Marketplace</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Welcome to your personalized research environment</p>', unsafe_allow_html=True)

    st.markdown("### Select your research persona:")
    st.markdown("This helps us tailor dataset recommendations and research insights to your field.")

    cols = st.columns(4)

    for i, (persona_id, persona) in enumerate(PERSONAS.items()):
        with cols[i]:
            with st.container():
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; border: 2px solid #E5E7EB; border-radius: 0.75rem;">
                    <div style="font-size: 3rem;">{persona['icon']}</div>
                    <h4 style="margin: 0.5rem 0;">{persona['name']}</h4>
                    <p style="color: #6B7280; font-size: 0.875rem;">{persona['focus']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Select {persona['name'].split()[0]}", key=f"select_{persona_id}", use_container_width=True):
                    st.session_state.user_persona = persona_id
                    st.session_state.show_onboarding = False
                    st.session_state.current_step = 1
                    st.rerun()


def render_step_indicator():
    """Render the step navigation indicator with consistent styling."""
    steps = [
        ("Access", "🔐", 1),
        ("Marketplace", "🌐", 2),
        ("Search", "🔍", 3),
        ("Curation", "⭐", 4),
        ("Insights", "📊", 5),
        ("Tools", "🔧", 6),
    ]

    # Create evenly-spaced columns with consistent sizing
    cols = st.columns([1, 1, 1, 1, 1, 1])

    for i, (name, icon, step_num) in enumerate(steps):
        with cols[i]:
            # Determine button styling based on state
            if step_num == st.session_state.current_step:
                button_type = "primary"
            else:
                button_type = "secondary"

            # Create button with consistent label format
            label = f"{icon}\n{name}"

            if st.button(
                label,
                key=f"step_{step_num}",
                use_container_width=True,
                type=button_type if step_num == st.session_state.current_step else "secondary"
            ):
                st.session_state.current_step = step_num
                st.rerun()


def render_dataset_card(dataset: dict, show_select: bool = True):
    """Render a dataset card with metadata."""
    is_selected = dataset['id'] in st.session_state.selected_datasets
    persona = st.session_state.user_persona
    relevance = dataset['relevance_scores'].get(persona, 50) if persona else 50

    with st.container():
        col1, col2 = st.columns([4, 1])

        with col1:
            # Header with name and access indicator
            access_icon = "🔓" if dataset['access_type'] == 'available' else "🔒"
            st.markdown(f"### {dataset['name']} {access_icon}")

            st.markdown(dataset['description'])

            # Tags
            tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in dataset['tags'][:5]])
            st.markdown(tags_html, unsafe_allow_html=True)

            # Metadata
            meta_cols = st.columns(4)
            with meta_cols[0]:
                st.markdown(f"**Size:** {dataset['size']}")
            with meta_cols[1]:
                st.markdown(f"**Format:** {dataset['format'].split(',')[0]}")
            with meta_cols[2]:
                st.markdown(f"**Samples:** {dataset['sample_count']:,}")
            with meta_cols[3]:
                st.markdown(f"**Provider:** {dataset['provider']}")

        with col2:
            st.metric("Relevance", f"{relevance}%")
            st.metric("Quality", f"{dataset['quality_score']}%")

            if show_select:
                if dataset['access_type'] == 'available':
                    if is_selected:
                        if st.button("✓ Selected", key=f"deselect_{dataset['id']}", type="primary", use_container_width=True):
                            st.session_state.selected_datasets.remove(dataset['id'])
                            st.rerun()
                    else:
                        if st.button("Select", key=f"select_{dataset['id']}", use_container_width=True):
                            st.session_state.selected_datasets.append(dataset['id'])
                            st.rerun()
                else:
                    st.button("Request Access", key=f"request_{dataset['id']}", use_container_width=True)

        st.divider()


def render_access_control():
    """Render Step 1: Access Control & Admin Dashboard."""
    st.markdown("## Access Control Dashboard")
    st.markdown("Administrative overview and system monitoring")

    # System metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Active Users",
            SYSTEM_METRICS['active_users'],
            "+12% from last month",
        )

    with col2:
        st.metric(
            "Pending Requests",
            SYSTEM_METRICS['pending_requests'],
            "23 awaiting approval",
        )

    with col3:
        st.metric(
            "System Load",
            f"{SYSTEM_METRICS['system_load']}%",
            "Optimal performance",
        )

    st.divider()

    # Large scale data management
    st.markdown("### Large Scale Data Management (Petabyte Scale)")

    scale_cols = st.columns(3)

    with scale_cols[0]:
        st.markdown("""
        <div style="background-color: #EFF6FF; padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 2rem;">⚡</div>
            <h4>Distributed Computing</h4>
            <p style="font-size: 0.875rem; color: #6B7280;">Apache Spark clusters for parallel processing</p>
            <p style="color: #2563EB; font-weight: 600;">Processing: 50 PB/hour</p>
        </div>
        """, unsafe_allow_html=True)

    with scale_cols[1]:
        st.markdown("""
        <div style="background-color: #ECFDF5; padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 2rem;">🗄️</div>
            <h4>Data Lake Architecture</h4>
            <p style="font-size: 0.875rem; color: #6B7280;">Tiered storage with hot/warm/cold management</p>
            <p style="color: #059669; font-weight: 600;">Capacity: 100+ PB</p>
        </div>
        """, unsafe_allow_html=True)

    with scale_cols[2]:
        st.markdown("""
        <div style="background-color: #F5F3FF; padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 2rem;">🛡️</div>
            <h4>Data Governance</h4>
            <p style="font-size: 0.875rem; color: #6B7280;">Automated compliance and lineage tracking</p>
            <p style="color: #7C3AED; font-weight: 600;">Security: SOC2 + GDPR</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Activity and API status
    col_activity, col_api = st.columns(2)

    with col_activity:
        st.markdown("### Recent Activity")
        for activity in RECENT_ACTIVITY:
            status_color = {
                'success': '🟢',
                'pending': '🟡',
                'info': '🔵'
            }.get(activity['status'], '⚪')

            st.markdown(f"""
            {status_color} **{activity['user']}** - {activity['action']}
            <span style="color: #6B7280; font-size: 0.875rem;">{activity['time']}</span>
            """, unsafe_allow_html=True)

    with col_api:
        st.markdown("### API Connectivity Status")
        for api in API_STATUS:
            status_color = '🟢' if api['status'] == 'Connected' else '🟡'
            st.markdown(f"""
            {status_color} **{api['name']}**
            {api['status']} • {api['latency']}
            """)

    st.divider()

    if st.button("Enter Marketplace →", type="primary", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()


def render_marketplace():
    """Render Step 2: Content Marketplace."""
    st.markdown("## Data Marketplace")
    st.markdown("Discover and access curated research datasets")

    # System metrics bar
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Total Storage", SYSTEM_METRICS['total_storage'])
    with metric_cols[1]:
        st.metric("Active Datasets", f"{SYSTEM_METRICS['active_datasets']:,}")
    with metric_cols[2]:
        st.metric("Daily Ingestion", SYSTEM_METRICS['daily_ingestion'])
    with metric_cols[3]:
        st.metric("Query Response", SYSTEM_METRICS['query_response'])

    st.divider()

    # Dataset grid
    for dataset in MOCK_DATASETS:
        render_dataset_card(dataset)

    if st.session_state.selected_datasets:
        st.success(f"✓ {len(st.session_state.selected_datasets)} dataset(s) selected")
        if st.button("Proceed to Search & Discovery →", type="primary"):
            st.session_state.current_step = 3
            st.rerun()


def render_search():
    """Render Step 3: Search & Discovery."""
    st.markdown("## Search & Discovery")
    st.markdown("AI-powered search with intelligent suggestions")

    # Search bar
    search_query = st.text_input(
        "Search datasets, research topics, or methodologies...",
        value=st.session_state.search_query,
        key="search_input",
    )
    st.session_state.search_query = search_query

    # Search suggestions based on persona
    if st.session_state.user_persona and search_query:
        persona_key = st.session_state.user_persona
        suggestions = []
        for key, suggs in SEARCH_SUGGESTIONS.items():
            if search_query.lower() in key.lower():
                suggestions.extend(suggs)

        if suggestions:
            st.markdown("**Suggestions:**")
            sugg_cols = st.columns(len(suggestions[:4]))
            for i, sugg in enumerate(suggestions[:4]):
                with sugg_cols[i]:
                    if st.button(sugg, key=f"sugg_{i}"):
                        st.session_state.search_query = sugg
                        st.rerun()

    st.divider()

    # Filter datasets
    filtered_datasets = MOCK_DATASETS
    if search_query:
        search_lower = search_query.lower()
        filtered_datasets = [
            d for d in MOCK_DATASETS
            if search_lower in d['name'].lower()
            or search_lower in d['description'].lower()
            or any(search_lower in tag.lower() for tag in d['tags'])
        ]

    st.markdown(f"**{len(filtered_datasets)} datasets found**")

    for dataset in filtered_datasets:
        render_dataset_card(dataset)

    if st.session_state.selected_datasets:
        if st.button("View Curated Recommendations →", type="primary"):
            st.session_state.current_step = 4
            st.rerun()


def render_curation():
    """Render Step 4: Curation & Recommendations."""
    st.markdown("## Curated Recommendations")
    st.markdown("Personalized dataset suggestions based on your research profile")

    persona = PERSONAS.get(st.session_state.user_persona, {})

    # Persona context
    st.info(f"""
    **Recommended for {persona.get('name', 'Researcher')}**
    These datasets have been curated based on your research interests and selected datasets.
    """)

    # Get recommended datasets (sorted by persona relevance)
    persona_id = st.session_state.user_persona
    recommended = sorted(
        MOCK_DATASETS,
        key=lambda d: d['relevance_scores'].get(persona_id, 0),
        reverse=True
    )[:5]

    for dataset in recommended:
        render_dataset_card(dataset)

    # Selection summary
    if st.session_state.selected_datasets:
        st.success(f"""
        **Selected Datasets ({len(st.session_state.selected_datasets)})**
        Ready to proceed with your research project using these datasets.
        """)

        if st.button("Generate Research Insights →", type="primary", use_container_width=True):
            st.session_state.current_step = 5
            st.rerun()
    else:
        st.warning("Select at least one dataset to generate research insights.")


def render_insights():
    """Render Step 5: AI-Powered Insights with visualizations."""
    from src.utils.visualizations import create_reproducibility_scorecard, create_agent_scores_chart

    st.markdown("## AI-Powered Research Insights")
    st.markdown("Intelligent analysis and research suggestions")

    persona_id = st.session_state.user_persona
    persona = PERSONAS.get(persona_id, {})

    # Reproducibility Scorecard - Main Feature
    st.markdown("### Reproducibility Scorecard")

    # Agent scores for visualization
    agent_scores = {
        "Analysis": 85,
        "Integrity": 92,
        "Testing": 78,
        "Collaboration": 88,
    }

    # Calculate overall score
    overall_score = sum(agent_scores.values()) / len(agent_scores)

    # Display overall score prominently
    score_cols = st.columns([1, 2, 1])
    with score_cols[1]:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 3rem; font-weight: bold; color: #4338CA;">{overall_score:.0f}</div>
            <div style="color: #6366F1; font-weight: 500;">Overall Reproducibility Score</div>
            <div style="font-size: 0.875rem; color: #6B7280; margin-top: 0.5rem;">Based on {len(st.session_state.selected_datasets)} selected datasets</div>
        </div>
        """, unsafe_allow_html=True)

    # Scorecard visualization
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        # Radar chart for dimensions
        dimension_scores = {
            "Methodology": 85,
            "Data Quality": 92,
            "Documentation": 75,
            "Reproducibility": 78,
            "Transparency": 88,
        }
        radar_fig = create_reproducibility_scorecard(dimension_scores)
        st.plotly_chart(radar_fig, use_container_width=True)

    with viz_col2:
        # Bar chart for agent scores
        bar_fig = create_agent_scores_chart(agent_scores)
        st.plotly_chart(bar_fig, use_container_width=True)

    st.divider()

    # Research approach recommendation
    st.markdown("""
    <div class="insight-box insight-blue">
        <h4>Recommended Research Approach</h4>
    </div>
    """, unsafe_allow_html=True)

    methodology = get_persona_methodology(persona_id)
    st.markdown(f"""
    Based on your selected datasets, we recommend a **longitudinal analysis approach**
    combining {methodology}.
    """)

    st.divider()

    # Research questions
    st.markdown("""
    <div class="insight-box insight-green">
        <h4>Potential Research Questions</h4>
    </div>
    """, unsafe_allow_html=True)

    questions = get_persona_research_questions(persona_id)
    for q in questions:
        st.markdown(f"• {q}")

    st.divider()

    # Methodology recommendations
    st.markdown("""
    <div class="insight-box insight-purple">
        <h4>Methodology Recommendations</h4>
    </div>
    """, unsafe_allow_html=True)

    methods = persona.get('methods', [])
    st.markdown(f"""
    Consider using statistical methods such as **{', '.join(methods[:2])}**,
    and complementary approaches including **{', '.join(methods[2:])}**.
    """)

    st.divider()

    # Detailed Agent Analysis
    st.markdown("### Detailed Agent Analysis")

    # All four agents in a grid
    agent_cols = st.columns(2)

    with agent_cols[0]:
        st.markdown("#### 🔬 Analysis Agent")
        st.progress(85)
        st.markdown("""
        **Score: 85/100** • Status: Pass
        - Statistical power: Adequate
        - Sample size: Sufficient for medium effects
        - Multiple comparison correction: Recommended
        """)

        st.markdown("#### 🧪 Testing Agent")
        st.progress(78)
        st.markdown("""
        **Score: 78/100** • Status: Warning
        - Experimental design: Good
        - Environment documentation: Needs improvement
        - Code reproducibility: Partially verified
        """)

    with agent_cols[1]:
        st.markdown("#### 🛡️ Integrity Agent")
        st.progress(92)
        st.markdown("""
        **Score: 92/100** • Status: Pass
        - Data provenance: Verified
        - FAIR compliance: 85%
        - Ethics documentation: Complete
        """)

        st.markdown("#### 🤝 Collaboration Agent")
        st.progress(88)
        st.markdown("""
        **Score: 88/100** • Status: Pass
        - Team coordination: Good
        - Authorship agreement: Present
        - Version control: Active
        """)

    st.divider()

    # Similar research and collaboration
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Similar Research")
        st.markdown("""
        **Related Study #1**
        "Longitudinal Analysis Methods in Research" - Nature Methods

        **Related Study #2**
        "Best Practices for Reproducible Research" - Journal of Applied Statistics

        **Related Study #3**
        "Open Science Framework Usage Patterns" - PLOS ONE
        """)

    with col2:
        st.markdown("### Collaboration Opportunities")
        st.markdown("""
        **Dr. Sarah Chen** • Match: 92%
        Stanford University - Similar datasets

        **Research Group Alpha** • Match: 85%
        MIT - Data analysis methods

        **Prof. Michael Torres** • Match: 78%
        Berkeley - Complementary expertise
        """)

    st.divider()

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Download Full Report", use_container_width=True):
            st.info("Report generation coming in Phase 3")
    with col2:
        if st.button("Proceed to Research Tools →", type="primary", use_container_width=True):
            st.session_state.current_step = 6
            st.rerun()


def render_tools():
    """Render Step 6: Research Tools Integration."""
    st.markdown("## Research & Analytical Tools")
    st.markdown("Connect to your preferred research environment")

    # Tool cards
    tool_cols = st.columns(3)

    for i, tool in enumerate(RESEARCH_TOOLS):
        with tool_cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #E5E7EB; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tool['icon']}</div>
                <h4 style="margin: 0;">{tool['name']}</h4>
                <p style="color: #6B7280; font-size: 0.875rem;">{tool['description']}</p>
                <p style="color: #059669; font-size: 0.875rem; font-weight: 600;">✓ {tool['status']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.button("Launch", key=f"launch_{i}", use_container_width=True)

    st.divider()

    # Documentation and collaboration tools
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Documentation")
        st.markdown("""
        - 📄 Research notebook templates
        - 📚 Automated citation generation
        - 📝 LaTeX integration for papers
        - 📋 Data dictionary templates
        """)

    with col2:
        st.markdown("### Collaboration")
        st.markdown("""
        - 👥 Real-time collaborative editing
        - ✅ Peer review workflows
        - 🔗 Repository sharing
        - 📊 Version control integration
        """)

    st.divider()

    # Summary
    persona = PERSONAS.get(st.session_state.user_persona, {})

    st.success(f"""
    ### Research Environment Ready!

    Your personalized research workspace has been configured with access to
    **{len(st.session_state.selected_datasets)} dataset(s)** and integrated analytical tools.

    **Persona:** {persona.get('name', 'Researcher')}
    **Focus:** {persona.get('focus', 'Research')}
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Launch Research Environment", type="primary", use_container_width=True):
            st.balloons()
            st.success("Environment launched! (Demo mode)")

    with col2:
        if st.button("Start New Project", use_container_width=True):
            st.session_state.selected_datasets = []
            st.session_state.current_step = 1
            st.rerun()


def main():
    """Main application entry point."""
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### Research Marketplace")

        if st.session_state.user_persona:
            persona = PERSONAS.get(st.session_state.user_persona, {})
            st.markdown(f"""
            **Current Persona:**
            {persona.get('icon', '')} {persona.get('name', '')}
            """)

            if st.session_state.selected_datasets:
                st.markdown(f"**Selected Datasets:** {len(st.session_state.selected_datasets)}")

            st.divider()

            if st.button("Change Persona"):
                st.session_state.show_onboarding = True
                st.session_state.user_persona = None
                st.session_state.current_step = 0
                st.rerun()

            if st.button("Reset Selection"):
                st.session_state.selected_datasets = []
                st.rerun()

        st.divider()
        st.markdown("""
        <div style="font-size: 0.75rem; color: #6B7280;">
        University Research Marketplace v1.0<br>
        Intelligent Research Lifecycle Orchestration
        </div>
        """, unsafe_allow_html=True)

    # Main content
    if st.session_state.show_onboarding:
        render_onboarding()
    else:
        # Step indicator
        render_step_indicator()
        st.divider()

        # Render current step
        if st.session_state.current_step == 1:
            render_access_control()
        elif st.session_state.current_step == 2:
            render_marketplace()
        elif st.session_state.current_step == 3:
            render_search()
        elif st.session_state.current_step == 4:
            render_curation()
        elif st.session_state.current_step == 5:
            render_insights()
        elif st.session_state.current_step == 6:
            render_tools()


if __name__ == "__main__":
    main()
