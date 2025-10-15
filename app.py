"""
EmpathZ AI Coordinator Demo
Streamlit application for crisis hotline call analysis and risk assessment
"""

import streamlit as st

# Import our modules
from data_demo import load_all_calls
from ui.layout import render_sidebar, render_footer
from ui.components import (
    render_dashboard_tab,
    render_call_list, 
    render_call_detail_view
)
from logic.analytics import compute_analytics

# Page configuration
st.set_page_config(
    page_title="EmpathZ AI Coordinator",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state with simplified structure"""
    if "calls_all" not in st.session_state:
        # Load all 10 calls immediately
        st.session_state.calls_all = load_all_calls()
        st.session_state.selected_tab = "dashboard"
        st.session_state.selected_call_id = None

def main():
    """Main application entry point"""
    initialize_session_state()
    
    # Render sidebar and get selected tab
    st.session_state.selected_tab = render_sidebar(st.session_state.selected_tab)
    
    # Main content area
    all_calls = st.session_state.calls_all
    
    # Conditional rendering based on selected tab
    if st.session_state.selected_tab == "dashboard":
        # Dashboard Tab
        st.title("📊 Dashboard")
        st.markdown("---")
        
        # Compute analytics for all calls
        analytics = compute_analytics(all_calls)
        render_dashboard_tab(analytics)
        
    elif st.session_state.selected_tab == "calls":
        # Call Records Tab
        st.title("📞 Call Records")
        st.markdown("---")
        
        # Gmail-style two-pane layout
        col_list, col_detail = st.columns([2, 3])
        
        # Left pane: Call records list
        with col_list:
            st.markdown("### Recent Calls")
            render_call_list(all_calls, st.session_state.selected_call_id)
        
        # Right pane: Selected call detail
        with col_detail:
            if st.session_state.selected_call_id:
                # Find selected call
                selected_call = next(
                    (call for call in all_calls 
                     if call["call_id"] == st.session_state.selected_call_id), 
                    None
                )
                
                if selected_call:
                    render_call_detail_view(selected_call)
                else:
                    st.info("Call not found")
            else:
                st.info("👈 Select a call from the list to view details")
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
