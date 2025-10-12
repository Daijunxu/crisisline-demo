"""
UI Components for EmpathZ AI Coordinator Demo
Handles call list, chat transcript, side panel, risk bars, and analytics
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from styles.theme import get_risk_color

def render_call_list(visible_calls: List[Dict[str, Any]], selected_call_id: Optional[str]):
    """
    Render the left-side call list with clickable items
    """
    if not visible_calls:
        st.info("No calls available")
        return
    
    for call in visible_calls:
        # Format call information
        duration_min = call["duration_sec"] // 60
        duration_sec = call["duration_sec"] % 60
        start_time = datetime.fromisoformat(call["started_at"]).strftime("%H:%M")
        end_time = datetime.fromisoformat(call["ended_at"]).strftime("%H:%M")
        
        # Create clickable call item
        call_key = f"call_{call['call_id']}"
        is_selected = selected_call_id == call["call_id"]
        
        # Display call information with animation
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button(
                f"{call['call_id']}",
                key=f"btn_{call_key}",
                help=f"Started: {start_time} | Duration: {duration_min}:{duration_sec:02d}",
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_call_id = call["call_id"]
                st.rerun()
        
        with col2:
            # Show risk indicator
            max_risk = max([
                call["risk"]["suicide"]["score"],
                call["risk"]["homicide"]["score"], 
                call["risk"]["self_harm"]["score"],
                call["risk"]["harm_others"]["score"]
            ])
            
            if max_risk >= 4:
                st.markdown("**🔴 HIGH RISK**")
            elif max_risk >= 2:
                st.markdown("**🟡 MODERATE**")
            else:
                st.markdown("**🟢 LOW**")
        
        # Call metadata
        st.caption(f"{start_time} - {end_time} | {duration_min}:{duration_sec:02d}")
        st.caption(f"{call['caller_profile']['age_range']} | {call['channel']}")
        
        if is_selected:
            st.markdown("""
            <div style="
                background-color: #2C4A6B;
                color: #F8F5ED;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 0.9em;
                font-weight: 500;
                text-align: center;
                margin: 8px 0;
            ">
                Selected
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()

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

def render_side_panel(call: Dict[str, Any], ui_phase: str):
    """
    Render the side panel with summary and risk evaluation
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
        HIGH RISK – ESCALATE TO SUPERVISOR
    </div>
    """, unsafe_allow_html=True)

def render_analytics_row(analytics: Dict[str, Any]):
    """
    Render the analytics cards at the bottom of the page
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="analytics-card">
            <div class="analytics-number">{}</div>
            <div class="analytics-label">Total Calls Analyzed</div>
        </div>
        """.format(analytics.get("total_calls", 0)), unsafe_allow_html=True)
    
    with col2:
        # Risk distribution
        risk_dist = analytics.get("risk_distribution", {})
        high_risk = risk_dist.get(4, 0) + risk_dist.get(5, 0)
        moderate_risk = risk_dist.get(2, 0) + risk_dist.get(3, 0)
        low_risk = risk_dist.get(0, 0) + risk_dist.get(1, 0)
        
        st.markdown("""
        <div class="analytics-card">
            <div class="analytics-number">🔴{} 🟡{} 🟢{}</div>
            <div class="analytics-label">Risk Distribution (High/Mod/Low)</div>
        </div>
        """.format(high_risk, moderate_risk, low_risk), unsafe_allow_html=True)
    
    with col3:
        avg_response = analytics.get("avg_response_time", 0)
        st.markdown("""
        <div class="analytics-card">
            <div class="analytics-number">{}s</div>
            <div class="analytics-label">Avg Response Time</div>
        </div>
        """.format(int(avg_response)), unsafe_allow_html=True)
