"""
Theme system for EmpathZ AI Coordinator Demo
Defines colors, fonts, spacing, and CSS injection for Streamlit
"""

import streamlit as st

# Color palette - EmpathZ brand theme based on logo
PRIMARY_BLUE = "#2C4A6B"          # Muted blue from logo (hand and text)
PRIMARY_BLUE_LIGHT = "#3B5A7A"    # Lighter blue for hover states
PRIMARY_CORAL = "#E87C60"         # Coral/orange from logo (speech bubble and heart)
PRIMARY_CORAL_LIGHT = "#F08970"   # Lighter coral for hover states
ALERT_RED = "#dc2626"             # Red for high-risk alerts
ALERT_RED_LIGHT = "#ef4444"       # Lighter red for risk bars

# Neutral colors - matching logo background
NEUTRAL_WHITE = "#ffffff"
NEUTRAL_CREAM = "#F8F5ED"         # Cream/beige background from logo
NEUTRAL_GRAY_50 = "#f9fafb"
NEUTRAL_GRAY_100 = "#f3f4f6"
NEUTRAL_GRAY_200 = "#e5e7eb"
NEUTRAL_GRAY_300 = "#d1d5db"
NEUTRAL_GRAY_400 = "#9ca3af"
NEUTRAL_GRAY_500 = "#6b7280"
NEUTRAL_GRAY_600 = "#4b5563"
NEUTRAL_GRAY_700 = "#374151"
NEUTRAL_GRAY_800 = "#1f2937"
NEUTRAL_GRAY_900 = "#111827"

# Risk bar colors (0-5 scale) - incorporating brand coral
RISK_COLORS = {
    0: NEUTRAL_GRAY_200,      # No risk - light gray
    1: "#fbbf24",             # Low risk - yellow
    2: PRIMARY_CORAL,         # Moderate risk - brand coral
    3: "#ef4444",             # High risk - red
    4: "#dc2626",             # Very high risk - dark red
    5: "#991b1b"              # Critical risk - darker red
}

# Spacing constants
SPACING_XS = "8px"
SPACING_SM = "12px"
SPACING_MD = "16px"
SPACING_LG = "24px"
SPACING_XL = "32px"
SPACING_XXL = "48px"

# Border radius
BORDER_RADIUS_SM = "4px"
BORDER_RADIUS_MD = "8px"
BORDER_RADIUS_LG = "12px"

def inject_theme_css():
    """Inject custom CSS theme into Streamlit"""
    css = f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');
        
        /* Global styles */
        .main {{
            padding-top: {SPACING_SM};
            padding-bottom: {SPACING_SM};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Poppins', sans-serif;
            color: {NEUTRAL_GRAY_800};
            margin-bottom: {SPACING_MD};
        }}
        
        /* Body text */
        .stApp, .stMarkdown, .stText, p, div {{
            font-family: 'Inter', sans-serif;
            color: {NEUTRAL_GRAY_700};
        }}
        
        /* Cards and containers */
        .card {{
            background: {NEUTRAL_WHITE};
            border-radius: {BORDER_RADIUS_MD};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: {SPACING_LG};
            margin-bottom: {SPACING_MD};
            border: 1px solid {NEUTRAL_GRAY_200};
        }}
        
        .card-elevated {{
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Call list items */
        .call-item {{
            background: {NEUTRAL_WHITE};
            border: 1px solid {NEUTRAL_GRAY_200};
            border-radius: {BORDER_RADIUS_MD};
            padding: {SPACING_MD};
            margin-bottom: {SPACING_SM};
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .call-item:hover {{
            border-color: {PRIMARY_BLUE};
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
        }}
        
        .call-item.selected {{
            border-color: {PRIMARY_BLUE};
            background: {PRIMARY_BLUE};
            color: {NEUTRAL_CREAM};
        }}
        
        /* Call item buttons */
        .call-item button {{
            background-color: {PRIMARY_BLUE} !important;
            color: {NEUTRAL_CREAM} !important;
            border-color: {PRIMARY_BLUE} !important;
        }}
        
        .call-item button:hover {{
            background-color: {PRIMARY_BLUE_LIGHT} !important;
            color: {NEUTRAL_CREAM} !important;
            border-color: {PRIMARY_BLUE_LIGHT} !important;
        }}
        
        /* Chat bubbles */
        .chat-bubble {{
            margin: {SPACING_SM} 0;
            padding: {SPACING_MD};
            border-radius: {BORDER_RADIUS_LG};
            max-width: 80%;
        }}
        
        .chat-bubble.caller {{
            background: {NEUTRAL_GRAY_100};
            margin-left: 0;
            margin-right: auto;
        }}
        
        .chat-bubble.responder {{
            background: {PRIMARY_BLUE};
            color: {NEUTRAL_WHITE};
            margin-left: auto;
            margin-right: 0;
        }}
        
        /* Transcript container */
        .transcript-container {{
            border: 1px solid {NEUTRAL_GRAY_200};
            border-radius: {BORDER_RADIUS_MD};
            background: {NEUTRAL_WHITE};
            margin: {SPACING_MD} 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .transcript-scrollable {{
            max-height: 400px;
            overflow-y: auto;
            padding: {SPACING_MD};
            scrollbar-width: thin;
            scrollbar-color: {NEUTRAL_GRAY_400} {NEUTRAL_GRAY_200};
        }}
        
        /* Custom scrollbar for webkit browsers */
        .transcript-scrollable::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .transcript-scrollable::-webkit-scrollbar-track {{
            background: {NEUTRAL_GRAY_200};
            border-radius: 4px;
        }}
        
        .transcript-scrollable::-webkit-scrollbar-thumb {{
            background: {NEUTRAL_GRAY_400};
            border-radius: 4px;
        }}
        
        .transcript-scrollable::-webkit-scrollbar-thumb:hover {{
            background: {NEUTRAL_GRAY_500};
        }}
        
        /* Risk bars */
        .risk-bar-container {{
            margin: {SPACING_SM} 0;
        }}
        
        .risk-bar {{
            display: flex;
            height: 24px;
            border-radius: {BORDER_RADIUS_SM};
            overflow: hidden;
            border: 1px solid {NEUTRAL_GRAY_300};
        }}
        
        .risk-segment {{
            flex: 1;
            transition: all 0.3s ease;
        }}
        
        /* Alert banner */
        .alert-banner {{
            background: {NEUTRAL_WHITE};
            color: {NEUTRAL_GRAY_900};
            border: 3px solid {ALERT_RED};
            padding: {SPACING_MD};
            margin: {SPACING_SM} 0;
            border-radius: {BORDER_RADIUS_MD};
            font-weight: 700;
            text-align: center;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
            font-size: 1.1rem;
        }}
        
        /* Side panel */
        .side-panel {{
            background: {NEUTRAL_WHITE};
            border: 1px solid {NEUTRAL_GRAY_200};
            border-radius: {BORDER_RADIUS_MD};
            padding: {SPACING_LG};
            margin-top: {SPACING_MD};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .side-panel-section {{
            margin-bottom: {SPACING_LG};
            padding-bottom: {SPACING_LG};
            border-bottom: 1px solid {NEUTRAL_GRAY_200};
        }}
        
        .side-panel-section:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        
        /* Analytics cards */
        .analytics-card {{
            background: {NEUTRAL_WHITE};
            border: 1px solid {NEUTRAL_GRAY_200};
            border-radius: {BORDER_RADIUS_MD};
            padding: {SPACING_LG};
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .analytics-number {{
            font-size: 2rem;
            font-weight: 700;
            color: {PRIMARY_BLUE};
            font-family: 'Poppins', sans-serif;
        }}
        
        .analytics-label {{
            color: {NEUTRAL_GRAY_600};
            font-size: 0.9rem;
            margin-top: {SPACING_XS};
        }}
        
        /* Buttons */
        .stButton > button {{
            border-radius: {BORDER_RADIUS_MD};
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        /* Collapsible sections */
        .collapsible {{
            background: {NEUTRAL_GRAY_50};
            border: 1px solid {NEUTRAL_GRAY_200};
            border-radius: {BORDER_RADIUS_MD};
            margin: {SPACING_SM} 0;
        }}
        
        .collapsible-header {{
            padding: {SPACING_MD};
            cursor: pointer;
            font-weight: 500;
            border-bottom: 1px solid {NEUTRAL_GRAY_200};
        }}
        
        .collapsible-content {{
            padding: {SPACING_MD};
            display: none;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease;
        }}
        
        @keyframes fillBar {{
            from {{ width: 0%; }}
            to {{ width: var(--fill-width); }}
        }}
        
        .risk-fill-animation {{
            animation: fillBar 0.8s ease;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .pulse-animation {{
            animation: pulse 0.6s ease;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .slide-in {{
            animation: slideIn 0.4s ease;
        }}
        
        /* Enhanced risk bar animations */
        .risk-segment {{
            transition: all 0.3s ease;
        }}
        
        .risk-segment:hover {{
            transform: scale(1.1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        /* Footer */
        .footer {{
            background: {NEUTRAL_GRAY_100};
            padding: {SPACING_LG};
            margin-top: {SPACING_XXL};
            border-top: 1px solid {NEUTRAL_GRAY_200};
            text-align: center;
            color: {NEUTRAL_GRAY_600};
            font-size: 0.9rem;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, {PRIMARY_CORAL} 0%, {PRIMARY_CORAL_LIGHT} 100%);
            color: {PRIMARY_BLUE};
            padding: {SPACING_XL};
            margin-bottom: {SPACING_LG};
            border-radius: {BORDER_RADIUS_MD};
            text-align: center;
        }}
        
        .header h1 {{
            color: {PRIMARY_BLUE};
            margin: 0;
            font-size: 1.8rem;
            font-weight: 600;
        }}
        
        .header p {{
            color: {NEUTRAL_CREAM};
            margin: {SPACING_SM} 0 0 0;
            font-size: 1rem;
        }}
        
        /* Ultra-aggressive button styling */
        button,
        button[data-testid],
        .stButton > button,
        .stButton > button[data-testid],
        div[data-testid="column"] button,
        div[data-testid="column"] .stButton > button,
        button[kind="primary"],
        button[kind="secondary"],
        button[kind="primary"][data-testid],
        button[kind="secondary"][data-testid],
        .stDownloadButton > button,
        .stDownloadButton button,
        .stDownloadButton > button[data-testid],
        .stDownloadButton button[data-testid],
        [data-testid="baseButton-secondary"],
        [data-testid="baseButton-primary"] {{
            background-color: {PRIMARY_BLUE} !important;
            color: {NEUTRAL_CREAM} !important;
            border: 1px solid {PRIMARY_BLUE} !important;
            border-radius: {BORDER_RADIUS_MD} !important;
            font-weight: 500 !important;
        }}
        
        /* Ultra-aggressive button hover styling */
        button:hover,
        button[data-testid]:hover,
        .stButton > button:hover,
        .stButton > button[data-testid]:hover,
        div[data-testid="column"] button:hover,
        div[data-testid="column"] .stButton > button:hover,
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover,
        button[kind="primary"][data-testid]:hover,
        button[kind="secondary"][data-testid]:hover,
        .stDownloadButton > button:hover,
        .stDownloadButton button:hover,
        .stDownloadButton > button[data-testid]:hover,
        .stDownloadButton button[data-testid]:hover,
        [data-testid="baseButton-secondary"]:hover,
        [data-testid="baseButton-primary"]:hover {{
            background-color: {PRIMARY_BLUE_LIGHT} !important;
            border-color: {PRIMARY_BLUE_LIGHT} !important;
            color: {NEUTRAL_CREAM} !important;
        }}
        
        /* Force text color with even more specificity */
        button *,
        .stButton > button *,
        button[data-testid] * {{
            color: {NEUTRAL_CREAM} !important;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
    
    # Add JavaScript to force button colors
    st.markdown("""
    <script>
    function forceButtonColors() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.style.backgroundColor = '#2C4A6B';
            button.style.color = '#F8F5ED';
            button.style.border = '1px solid #2C4A6B';
        });
        
        const buttonTexts = document.querySelectorAll('button *');
        buttonTexts.forEach(text => {
            text.style.color = '#F8F5ED';
        });
    }
    
    // Run on page load
    forceButtonColors();
    
    // Run when new content is added
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                forceButtonColors();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    </script>
    """, unsafe_allow_html=True)

def get_risk_color(score: int) -> str:
    """Get color for risk score (0-5)"""
    return RISK_COLORS.get(max(0, min(5, score)), NEUTRAL_GRAY_200)

def apply_card_style():
    """Apply card styling to current container"""
    return f"""
    <div class="card">
    """

def apply_alert_style():
    """Apply alert banner styling"""
    return f"""
    <div class="alert-banner">
    """

def apply_side_panel_style():
    """Apply side panel styling"""
    return f"""
    <div class="side-panel">
    """
