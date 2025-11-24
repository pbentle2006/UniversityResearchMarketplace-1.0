"""Visualization components for the Research Marketplace."""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any


def create_reproducibility_scorecard(scores: Dict[str, float]) -> go.Figure:
    """
    Create a radar chart showing reproducibility scores across dimensions.

    Args:
        scores: Dictionary mapping dimension names to scores (0-100)

    Returns:
        Plotly figure with radar chart
    """
    categories = list(scores.keys())
    values = list(scores.values())

    # Close the radar chart
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.3)',
        line=dict(color='rgb(99, 102, 241)', width=2),
        name='Your Score'
    ))

    # Add benchmark line
    benchmark = [75] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=benchmark,
        theta=categories,
        fill='none',
        line=dict(color='rgba(156, 163, 175, 0.5)', width=1, dash='dash'),
        name='Benchmark'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=40, b=60),
        height=400,
    )

    return fig


def create_agent_scores_chart(agent_scores: Dict[str, float]) -> go.Figure:
    """
    Create a horizontal bar chart showing agent scores.

    Args:
        agent_scores: Dictionary mapping agent names to scores

    Returns:
        Plotly figure with bar chart
    """
    agents = list(agent_scores.keys())
    scores = list(agent_scores.values())

    # Color based on score
    colors = []
    for score in scores:
        if score >= 80:
            colors.append('#10B981')  # Green
        elif score >= 60:
            colors.append('#F59E0B')  # Yellow
        else:
            colors.append('#EF4444')  # Red

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=scores,
        y=agents,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=[f'{s:.0f}%' for s in scores],
        textposition='inside',
        textfont=dict(color='white', size=12),
    ))

    fig.update_layout(
        xaxis=dict(
            title='Score',
            range=[0, 100],
            ticksuffix='%',
        ),
        yaxis=dict(
            title='',
            autorange='reversed',
        ),
        margin=dict(l=120, r=40, t=20, b=40),
        height=250,
        showlegend=False,
    )

    return fig


def create_findings_summary(findings: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a pie chart showing findings by severity.

    Args:
        findings: List of finding dictionaries with 'severity' key

    Returns:
        Plotly figure with pie chart
    """
    severity_counts = {
        'success': 0,
        'info': 0,
        'warning': 0,
        'error': 0,
    }

    for finding in findings:
        severity = finding.get('severity', 'info')
        if severity in severity_counts:
            severity_counts[severity] += 1

    labels = ['Success', 'Info', 'Warning', 'Error']
    values = [
        severity_counts['success'],
        severity_counts['info'],
        severity_counts['warning'],
        severity_counts['error'],
    ]
    colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']

    # Filter out zero values
    filtered_data = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]

    if not filtered_data:
        filtered_data = [('No findings', 1, '#9CA3AF')]

    labels, values, colors = zip(*filtered_data)

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textinfo='label+value',
        textfont=dict(size=11),
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=250,
        showlegend=False,
    )

    return fig


def create_timeline_chart(milestones: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a Gantt-style timeline chart for project milestones.

    Args:
        milestones: List of milestone dictionaries with 'name', 'start', 'end', 'status'

    Returns:
        Plotly figure with timeline
    """
    if not milestones:
        # Return empty figure
        fig = go.Figure()
        fig.update_layout(
            annotations=[dict(
                text="No milestones defined",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )],
            height=200,
        )
        return fig

    # Create DataFrame for Gantt chart
    import pandas as pd

    df = pd.DataFrame(milestones)

    status_colors = {
        'completed': '#10B981',
        'in_progress': '#3B82F6',
        'pending': '#9CA3AF',
    }

    fig = px.timeline(
        df,
        x_start='start',
        x_end='end',
        y='name',
        color='status',
        color_discrete_map=status_colors,
    )

    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        height=200,
        margin=dict(l=100, r=20, t=20, b=40),
    )

    return fig


def create_collaboration_network(team_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a network visualization of team collaborations.

    Args:
        team_data: List of team member dictionaries

    Returns:
        Plotly figure with network graph
    """
    if not team_data or len(team_data) < 2:
        fig = go.Figure()
        fig.update_layout(
            annotations=[dict(
                text="Add team members to visualize network",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )],
            height=300,
        )
        return fig

    # Simple circular layout for team members
    import math

    n = len(team_data)
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = math.cos(angle)
        y = math.sin(angle)
        positions.append((x, y))

    # Create edges (simplified: all connected to center)
    edge_x = []
    edge_y = []
    for i, pos in enumerate(positions):
        edge_x.extend([0, pos[0], None])
        edge_y.extend([0, pos[1], None])

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=1, color='#D1D5DB'),
        hoverinfo='none',
    ))

    # Center node (project)
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode='markers+text',
        marker=dict(size=30, color='#6366F1'),
        text=['Project'],
        textposition='middle center',
        textfont=dict(color='white', size=10),
        hoverinfo='text',
        hovertext='Project Hub',
    ))

    # Team member nodes
    node_x = [pos[0] for pos in positions]
    node_y = [pos[1] for pos in positions]
    node_text = [m.get('name', f'Member {i+1}') for i, m in enumerate(team_data)]

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(size=20, color='#10B981'),
        text=node_text,
        textposition='top center',
        textfont=dict(size=9),
        hoverinfo='text',
        hovertext=[m.get('role', 'Team Member') for m in team_data],
    ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
    )

    return fig
