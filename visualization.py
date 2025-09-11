from utils import get_api_keys
import plotly.graph_objects as go

def create_pipeline_visualization(system_type: str, route_decision: str = None, processing_steps: list = None):
    """Create enhanced pipeline visualization"""
    fig = go.Figure()
    
    if system_type == "traditional":
        # Traditional RAG - Simple linear flow
        fig.add_trace(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["User Query", "Fixed Router", "Local Documents", "Basic LLM", "Answer"],
                color=["#ffcccc", "#ff9999", "#ff6666", "#ff3333", "#ff0000"]
            ),
            link=dict(
                source=[0, 1, 2, 3],
                target=[1, 2, 3, 4],
                value=[1, 1, 1, 1],
                color=["#ff6666", "#ff6666", "#ff6666", "#ff6666"]
            )
        ))
        title = "Traditional RAG Pipeline - Fixed & Simple"
        
    else:
        # Agentic RAG - Intelligent branching flow
        if route_decision == "LOCAL":
            colors = ["#ccffcc", "#99ff99", "#66ff66", "#33ff33", "#00ff00"]
            link_colors = ["#66ff66", "#66ff66", "#66ff66", "#66ff66"]
            source_label = "Local Source"
        elif route_decision == "WEB":
            colors = ["#cce5ff", "#99d6ff", "#66c7ff", "#33b8ff", "#00a9ff"]
            link_colors = ["#66c7ff", "#66c7ff", "#66c7ff", "#66c7ff"]
            source_label = "Web Source"
        else:  # HYBRID
            colors = ["#e0f7fa", "#b2ebf2", "#80deea", "#4dd0e1", "#26c6da"]
            link_colors = ["#80deea", "#80deea", "#80deea", "#80deea"]
            source_label = "Local + Web Sources"
            
        fig.add_trace(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["User Query", "Smart Router", source_label, "Advanced LLM", "Enhanced Answer"],
                color=colors
            ),
            link=dict(
                source=[0, 1, 2, 3],
                target=[1, 2, 3, 4],
                value=[1, 1, 1, 1],
                color=link_colors
            )
        ))
        title = f"Agentic RAG Pipeline - {route_decision} Route"
    
    fig.update_layout(
        title_text=title,
        font_size=12,
        height=300,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_processing_steps_visual(steps: list, system_type: str):
    """Create visual representation of processing steps"""
    step_html = "<div style='margin: 1rem 0;'>"
    
    for i, step in enumerate(steps, 1):
        if system_type == "traditional":
            step_class = "pipeline-step step-traditional"
        else:
            step_class = "pipeline-step step-agentic"
            
        step_html += f"<span class='{step_class}'>{i}. {step}</span>"
        if i < len(steps):
            step_html += " → "
    
    step_html += "</div>"
    return step_html
