"""
UI Components for EmpathZ AI Coordinator Demo
Handles call list, chat transcript, side panel, risk bars, and analytics
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from styles.theme import get_risk_color, get_risk_level, get_risk_badge_class, RISK_LOW_COLOR, RISK_MOD_COLOR, RISK_HIGH_COLOR
import plotly.graph_objects as go

def render_dashboard_tab(analytics: Dict[str, Any]):
    """
    Render the Dashboard tab with KPI cards and risk distribution chart
    Args:
        analytics: Dictionary containing analytics data (total_calls, avg_response_time, risk_distribution)
    """
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # KPI Cards Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_kpi_card("Today's Total Calls", analytics.get("total_calls", 0), "")
    
    with col2:
        avg_time = analytics.get("avg_response_time", 0)
        render_kpi_card("Avg Response Time", f"{int(avg_time)}s", "")
    
    with col3:
        # Calculate high risk percentage
        risk_dist = analytics.get("risk_distribution", {})
        total = sum(risk_dist.values())
        high_risk_count = risk_dist.get(4, 0) + risk_dist.get(5, 0)
        high_risk_pct = (high_risk_count / total * 100) if total > 0 else 0
        render_kpi_card("High Risk %", f"{high_risk_pct:.1f}%", "")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Risk Distribution Chart
    st.markdown("---")
    st.markdown("### Risk Distribution — Today")
    render_risk_distribution_chart(analytics.get("risk_distribution", {}))

def render_kpi_card(label: str, value: str, subtitle: str = ""):
    """
    Render a KPI card with a large number and label
    Args:
        label: The label for the metric
        value: The value to display (as string for formatting flexibility)
        subtitle: Optional subtitle text
    """
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-number">{value}</div>
        <div class="kpi-label">{label}</div>
        {f'<div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_risk_distribution_chart(risk_distribution: Dict[int, int]):
    """
    Render a horizontal bar chart showing risk distribution
    Args:
        risk_distribution: Dictionary mapping risk scores (0-5) to counts
    """
    # Group into LOW (0-1), MOD (2-3), HIGH (4-5)
    low_count = risk_distribution.get(0, 0) + risk_distribution.get(1, 0)
    mod_count = risk_distribution.get(2, 0) + risk_distribution.get(3, 0)
    high_count = risk_distribution.get(4, 0) + risk_distribution.get(5, 0)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=['Risk Level'],
        x=[low_count],
        name='Low Risk',
        orientation='h',
        marker=dict(color=RISK_LOW_COLOR),
        text=[f'{low_count} calls'],
        textposition='inside',
        hovertemplate='<b>Low Risk</b><br>%{x} calls<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=['Risk Level'],
        x=[mod_count],
        name='Moderate Risk',
        orientation='h',
        marker=dict(color=RISK_MOD_COLOR),
        text=[f'{mod_count} calls'],
        textposition='inside',
        hovertemplate='<b>Moderate Risk</b><br>%{x} calls<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=['Risk Level'],
        x=[high_count],
        name='High Risk',
        orientation='h',
        marker=dict(color=RISK_HIGH_COLOR),
        text=[f'{high_count} calls'],
        textposition='inside',
        hovertemplate='<b>High Risk</b><br>%{x} calls<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(title="Number of Calls"),
        yaxis=dict(showticklabels=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_call_list(visible_calls: List[Dict[str, Any]], selected_call_id: Optional[str]):
    """
    Render Gmail-style call list with call ID, subject line, time, and risk badge
    Args:
        visible_calls: List of call dictionaries
        selected_call_id: Currently selected call ID
    """
    if not visible_calls:
        st.info("No calls available")
        return
    
    st.markdown('<div class="call-list-container">', unsafe_allow_html=True)
    
    for call in visible_calls:
        # Get max risk score
        max_risk = max([
            call["risk"]["suicide"]["score"],
            call["risk"]["homicide"]["score"], 
            call["risk"]["self_harm"]["score"],
            call["risk"]["harm_others"]["score"]
        ])
        
        # Get presenting problem as subject line (truncated)
        presenting_problem = call["summary"]["sections"].get("presenting_problem", "No summary available")
        if len(presenting_problem) > 80:
            presenting_problem = presenting_problem[:80] + "..."
        
        # Format time
        start_time = datetime.fromisoformat(call["started_at"]).strftime("%H:%M")
        
        # Get risk level and badge class
        risk_level = get_risk_level(max_risk)
        risk_badge_class = get_risk_badge_class(max_risk)
        
        # Determine if selected
        is_selected = selected_call_id == call["call_id"]
        selected_class = "selected" if is_selected else ""
        
        # Risk dot color
        if max_risk <= 1:
            risk_dot_color = RISK_LOW_COLOR
        elif max_risk <= 3:
            risk_dot_color = RISK_MOD_COLOR
        else:
            risk_dot_color = RISK_HIGH_COLOR
        
        # Create clickable call item
        call_html = f"""
        <div class="call-item {selected_class}" onclick="document.getElementById('call_btn_{call["call_id"]}').click()">
            <div style="flex: 1;">
                <div class="call-id">{call["call_id"]}</div>
                <div class="call-subject">{presenting_problem}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div class="call-time">{start_time}</div>
                <div class="risk-badge {risk_badge_class}">
                    <div class="risk-dot" style="background-color: {risk_dot_color};"></div>
                    {risk_level}
                </div>
            </div>
        </div>
        """
        st.markdown(call_html, unsafe_allow_html=True)
        
        # Hidden button for interactivity
        if st.button(call["call_id"], key=f"call_btn_{call['call_id']}", type="secondary", 
                    help=f"View details for {call['call_id']}", 
                    label_visibility="collapsed"):
            st.session_state.selected_call_id = call["call_id"]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_transcript(turns: List[Dict[str, str]]):
    """
    Render the chat transcript with conversation bubbles
    """
    if not turns:
        st.info("No transcript available")
        return
    
    # Inject CSS styles for chat bubbles
    st.markdown("""
    <style>
    .chat-bubble {
        margin: 12px 0;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 75%;
        word-wrap: break-word;
    }
    .chat-bubble-caller {
        background: #f3f4f6;
        margin-left: 0;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    .chat-bubble-responder {
        background: #F08970;
        color: white;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 4px;
    }
    .chat-bubble-speaker {
        font-weight: bold;
        font-size: 0.85em;
        margin-bottom: 4px;
        opacity: 0.8;
    }
    .chat-bubble-text {
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render each message as a separate bubble
    for turn in turns:
        speaker = turn["speaker"]
        text = turn["text"]
        
        if speaker == "caller":
            st.markdown(f"""
            <div class="chat-bubble chat-bubble-caller">
                <div class="chat-bubble-speaker">Caller</div>
                <div class="chat-bubble-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble chat-bubble-responder">
                <div class="chat-bubble-speaker">Responder</div>
                <div class="chat-bubble-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

def render_call_detail_view(call: Dict[str, Any]):
    """
    Render the call detail view with split layout: transcript (left) | AI outputs (right)
    Args:
        call: Selected call dictionary
    """
    from logic.risk_rules import has_red_alert
    
    # Show RED alert banner if high risk
    if has_red_alert(call["risk"]):
        render_alert_banner()
    
    # Split view: Left half (transcript) | Right half (AI outputs)
    col_transcript, col_ai = st.columns([1, 1])
    
    with col_transcript:
        st.markdown("### Call Transcript")
        render_chat_transcript(call["turns"])
    
    with col_ai:
        # PDF download button in top-right
        col_header, col_btn = st.columns([3, 1])
        with col_header:
            st.markdown("### AI Analysis")
        with col_btn:
            if st.button("📄 PDF", key="download_btn", help="Download full report"):
                try:
                    from logic.pdf_report import generate_pdf_report, create_download_filename
                    import tempfile
                    import os
                    
                    # Generate PDF
                    filename = create_download_filename(call)
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    
                    pdf_path = generate_pdf_report(call, temp_path)
                    
                    # Offer download
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f.read(),
                            file_name=filename,
                            mime="application/pdf",
                            key="pdf_download"
                        )
                    
                    st.success("✅ Report generated successfully!")
                    
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
        
        # AI Summary
        st.markdown("#### Case Summary")
        render_summary_section(call["summary"])
        
        st.markdown("---")
        
        # AI Assessment
        st.markdown("#### Risk Assessment")
        render_risk_evaluation(call["risk"])

def render_side_panel(call: Dict[str, Any], ui_phase: str):
    """
    Render the side panel with summary and risk evaluation (legacy function, kept for compatibility)
    """
    
    # Side panel header with download button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("AI Analysis")
    with col2:
        if st.button("Download Report", key="download_btn"):
            try:
                from logic.pdf_report import generate_pdf_report, create_download_filename
                import tempfile
                import os
                
                # Generate PDF
                filename = create_download_filename(call)
                temp_path = os.path.join(tempfile.gettempdir(), filename)
                
                pdf_path = generate_pdf_report(call, temp_path)
                
                # Offer download
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f.read(),
                        file_name=filename,
                        mime="application/pdf",
                        key="pdf_download"
                    )
                
                st.success("✅ Report generated successfully!")
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.error("Please try again or contact support if the issue persists.")
    
    # Summary section
    st.markdown("### Case Summary")
    
    if ui_phase in ["summary_generating", "idle"] and ui_phase != "summary_done":
        if ui_phase == "summary_generating":
            st.info("Generating Summary...")
        else:
            st.info("Summary will appear after analysis")
    else:
        render_summary_section(call["summary"])
    
    st.divider()
    
    # Risk evaluation section
    st.markdown("### Risk Assessment")
    
    if ui_phase in ["risk_evaluating", "summary_generating", "idle"] and ui_phase != "complete":
        if ui_phase == "risk_evaluating":
            st.info("Evaluating Risk...")
        else:
            st.info("Risk assessment will appear after analysis")
    else:
        render_risk_evaluation(call["risk"])

def render_summary_section(summary: Dict[str, Any]):
    """
    Render the case report style summary
    """
    sections = summary.get("sections", {})
    
    # Caller Profile
    if sections.get("caller_profile"):
        st.markdown("**Caller Profile:**")
        st.write(sections["caller_profile"])
        st.markdown("")
    
    # Presenting Problem
    if sections.get("presenting_problem"):
        st.markdown("**Presenting Problem:**")
        st.write(sections["presenting_problem"])
        st.markdown("")
    
    # Context & Timeline
    if sections.get("context_timeline"):
        st.markdown("**Context & Timeline:**")
        st.write(sections["context_timeline"])
        st.markdown("")
    
    # Risk Factors
    if sections.get("risk_factors"):
        st.markdown("**Risk Factors:**")
        st.write(sections["risk_factors"])
        st.markdown("")
    
    # Protective Factors
    if sections.get("protective_factors"):
        st.markdown("**Protective Factors:**")
        st.write(sections["protective_factors"])
        st.markdown("")
    
    # Interventions
    if sections.get("interventions"):
        st.markdown("**Interventions Provided:**")
        st.write(sections["interventions"])
        st.markdown("")
    
    # Outcome
    if sections.get("outcome"):
        st.markdown("**Outcome:**")
        st.write(sections["outcome"])
        st.markdown("")
    
    # Safety Plan
    if sections.get("safety_plan"):
        st.markdown("**Safety Plan & Referrals:**")
        st.write(sections["safety_plan"])

def render_risk_evaluation(risk: Dict[str, Any]):
    """
    Render the risk evaluation with bars and reasoning
    """
    risk_dimensions = ["suicide", "homicide", "self_harm", "harm_others"]
    dimension_labels = {
        "suicide": "Suicide Risk",
        "homicide": "Homicide Risk", 
        "self_harm": "Self-Harm Risk",
        "harm_others": "Harm to Others"
    }
    
    for dimension in risk_dimensions:
        if dimension in risk:
            score = risk[dimension]["score"]
            explanation = risk[dimension]["explanation"]
            quotes = risk[dimension]["reason_quotes"]
            
            st.markdown(f"**{dimension_labels[dimension]}**")
            
            # Render risk bar
            render_risk_bar(dimension, score, explanation, quotes)
            st.markdown("")

def render_risk_bar(dimension_name: str, score: int, explanation: str, quotes: List[str]):
    """
    Render a single risk bar with collapsible reasoning
    """
    # Create risk bar visualization
    segments = []
    for i in range(5):
        if i < score:
            color = get_risk_color(score)
            segments.append(f'<div class="risk-segment" style="background-color: {color};"></div>')
        else:
            segments.append('<div class="risk-segment" style="background-color: #e5e7eb;"></div>')
    
    risk_bar_html = f'''
    <div class="risk-bar-container fade-in">
        <div class="risk-bar">
            {"".join(segments)}
        </div>
        <p style="margin-top: 8px; font-weight: 500;" class="pulse-animation">Score: {score}/5</p>
    </div>
    '''
    
    st.markdown(risk_bar_html, unsafe_allow_html=True)
    
    # Collapsible reasoning section
    with st.expander("Show Reasoning", expanded=False):
        st.write(explanation)
        
        if quotes:
            st.markdown("**Key Quotes:**")
            for quote in quotes:
                st.markdown(f"> *{quote}*")

def render_alert_banner():
    """
    Render the RED alert banner for high-risk situations
    """
    st.markdown("""
    <div class="alert-banner">
        ⚠️ HIGH RISK – ESCALATE TO SUPERVISOR
    </div>
    """, unsafe_allow_html=True)
