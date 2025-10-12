"""
Layout components for EmpathZ AI Coordinator Demo
Handles page layout, header, footer, and column structure
"""

import streamlit as st
from styles.theme import inject_theme_css

def render_header():
    """Render the application header with branding and tagline"""
    inject_theme_css()
    
    st.markdown("""
    <div class="header">
        <h1>EmpathZ AI Coordinator</h1>
        <p>Summarizing and Assessing Crisis Calls in Real Time</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render the persistent footer with disclaimer and copyright"""
    st.markdown("""
    <div class="footer">
        <p>Demo – Not Real Patient Data · © 2025 EmpathZ Demo v1.0</p>
    </div>
    """, unsafe_allow_html=True)

def create_two_column_layout():
    """
    Create the main two-column layout for the application
    Returns left column (30%) and right column (70%)
    """
    col1, col2 = st.columns([3, 7])
    return col1, col2

def create_three_column_layout():
    """
    Create a three-column layout for analytics cards
    Returns three equal columns
    """
    col1, col2, col3 = st.columns(3)
    return col1, col2, col3

def create_side_panel_layout():
    """
    Create layout for the side panel with two stacked sections
    Returns container for the side panel
    """
    container = st.container()
    return container
