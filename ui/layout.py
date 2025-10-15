"""
Layout components for EmpathZ AI Coordinator Demo
Handles page layout, sidebar, footer, and column structure
"""

import streamlit as st
from styles.theme import inject_theme_css

def render_sidebar(selected_tab: str):
    """
    Render the fixed-width vertical sidebar with navigation tabs
    Args:
        selected_tab: Currently selected tab ("dashboard" or "calls")
    Returns:
        The new selected tab based on user interaction
    """
    inject_theme_css()
    
    # Using Streamlit's actual sidebar for tab buttons
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        st.markdown("")  # Add some spacing
        
        if st.button("📊 Dashboard", key="nav_dashboard", 
                    type="primary" if selected_tab == "dashboard" else "secondary",
                    use_container_width=True):
            selected_tab = "dashboard"
        
        st.markdown("")  # Add some spacing between buttons
            
        if st.button("📞 Call Records", key="nav_calls",
                    type="primary" if selected_tab == "calls" else "secondary", 
                    use_container_width=True):
            selected_tab = "calls"
        
        # Version note at bottom
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.75rem; color: #6b7280; margin-top: 2rem;">
            EmpathZ Demo<br/>v1.0
        </div>
        """, unsafe_allow_html=True)
    
    return selected_tab

def render_footer():
    """Render the persistent footer with disclaimer and copyright"""
    st.markdown("""
    <div class="footer">
        <p>Demo – Not Real Patient Data · © 2025 EmpathZ Demo v1.0</p>
    </div>
    """, unsafe_allow_html=True)
