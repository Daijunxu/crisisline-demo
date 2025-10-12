"""
EmpathZ AI Coordinator Demo
Streamlit application for crisis hotline call analysis and risk assessment
"""

import streamlit as st
from datetime import datetime, timezone, timedelta
import time

# Import our modules
from data_demo import load_all_calls, validate_call_schema
from ui.layout import render_header, render_footer, create_two_column_layout
from ui.components import (
    render_call_list, 
    render_chat_transcript, 
    render_side_panel,
    render_alert_banner,
    render_analytics_row
)
from logic.analytics import compute_analytics
from logic.risk_rules import has_red_alert

# Page configuration
st.set_page_config(
    page_title="EmpathZ AI Coordinator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if "calls_all" not in st.session_state:
        st.session_state.calls_all = load_all_calls()
        # Initially show first 2 calls
        st.session_state.visible_call_ids = {call["call_id"] for call in st.session_state.calls_all[:2]}
        st.session_state.selected_call_id = None
        # Remaining calls for simulation
        st.session_state.pending_simulation_queue = st.session_state.calls_all[2:]
        st.session_state.ui_phase = "idle"

def simulate_new_analysis():
    """Simulate processing a new call with delays and animations"""
    if not st.session_state.pending_simulation_queue:
        st.warning("All sample calls loaded.")
        return
    
    # Pop next call
    next_call = st.session_state.pending_simulation_queue.pop(0)
    st.session_state.visible_call_ids.add(next_call["call_id"])
    st.session_state.selected_call_id = next_call["call_id"]
    
    # Phase 1: Generate summary
    st.session_state.ui_phase = "summary_generating"
    with st.spinner("Generating Summary…"):
        time.sleep(2)
    st.session_state.ui_phase = "summary_done"
    
    # Phase 2: Evaluate risk
    st.session_state.ui_phase = "risk_evaluating"
    with st.spinner("Evaluating Risk…"):
        time.sleep(2)
    st.session_state.ui_phase = "complete"
    
    # Recompute analytics (with animation effects)
    st.rerun()

def main():
    """Main application entry point"""
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Get visible calls
    visible_calls = [call for call in st.session_state.calls_all 
                    if call["call_id"] in st.session_state.visible_call_ids]
    
    # Render alert banner if needed
    selected_call = None
    if st.session_state.selected_call_id:
        selected_call = next((call for call in visible_calls 
                            if call["call_id"] == st.session_state.selected_call_id), None)
        if selected_call and has_red_alert(selected_call["risk"]):
            render_alert_banner()
    
    # Analytics dashboard at top
    st.markdown("---")
    analytics = compute_analytics(visible_calls)
    render_analytics_row(analytics)
    st.markdown("---")
    
    # Create two-column layout
    col_left, col_right = create_two_column_layout()
    
    # Left column: Call list
    with col_left:
        # Recent Calls header with Simulate button on the same line
        col_header, col_button = st.columns([3, 1])
        with col_header:
            st.subheader("Recent Calls")
        with col_button:
            if st.button("Simulate Data", type="primary"):
                simulate_new_analysis()
        
        render_call_list(visible_calls, st.session_state.selected_call_id)
    
    # Right column: Transcript and side panel
    with col_right:
        if selected_call:
            # Chat transcript
            st.subheader("Call Transcript")
            render_chat_transcript(selected_call["turns"])
            
            # Simple divider line
            st.markdown("---")
            
            # Side panel with summary and risk evaluation
            render_side_panel(selected_call, st.session_state.ui_phase)
        else:
            st.info("Select a call from the list to view transcript and analysis")
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
