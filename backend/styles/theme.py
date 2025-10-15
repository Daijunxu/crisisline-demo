"""
Theme system for EmpathZ AI Coordinator Demo
Defines colors, fonts, spacing, and CSS injection for Streamlit
"""

import streamlit as st

# Color palette - Light enterprise style
PRIMARY_BLUE = "#2563eb"          # Primary blue for accents
PRIMARY_BLUE_DARK = "#1d4ed8"     # Darker blue for hover states
PRIMARY_BLUE_LIGHT = "#3b82f6"    # Lighter blue
SECONDARY_BLUE = "#60a5fa"        # Secondary blue

# Neutral colors - Light enterprise theme
NEUTRAL_WHITE = "#ffffff"
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

# Risk colors - per design spec
RISK_LOW_COLOR = "#22C55E"        # Green for low risk
RISK_MOD_COLOR = "#FACC15"        # Yellow for moderate risk
RISK_HIGH_COLOR = "#DC2626"       # Red for high risk

# Risk bar colors (0-5 scale)
RISK_COLORS = {
    0: RISK_LOW_COLOR,            # No risk - green
    1: RISK_LOW_COLOR,            # Low risk - green
    2: RISK_MOD_COLOR,            # Moderate risk - yellow
    3: RISK_MOD_COLOR,            # Moderate risk - yellow
    4: RISK_HIGH_COLOR,           # High risk - red
    5: RISK_HIGH_COLOR            # Critical risk - red
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
        /* Import Google Fonts - Poppins for headings, Inter for body */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');
        
        /* Global styles */
        .main {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            background-color: {NEUTRAL_WHITE};
        }}
        
        /* Hide default Streamlit menu */
        #MainMenu {{visibility: hidden;}}
        
        /* Force sidebar to be visible */
        section[data-testid="stSidebar"] {{
            visibility: visible !important;
            display: block !important;
            width: 250px !important;
            min-width: 250px !important;
        }}
        
        section[data-testid="stSidebar"] > div {{
            visibility: visible !important;
            display: block !important;
        }}
        
        /* Hide the sidebar collapse button since we want it always open */
        button[kind="header"] {{
            display: none !important;
        }}
        
        /* Headers - Poppins font */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Poppins', sans-serif;
            color: {NEUTRAL_GRAY_800};
            margin-bottom: {SPACING_MD};
        }}
        
        /* Body text - Inter font */
        .stApp, .stMarkdown, .stText, p, div, span {{
            font-family: 'Inter', sans-serif;
            color: {NEUTRAL_GRAY_700};
        }}
        
        /* Sidebar Container */
        .sidebar-container {{
            position: fixed;
            left: 0;
            top: 0;
            width: 250px;
            height: 100vh;
            background-color: {NEUTRAL_WHITE};
            border-right: 1px solid {NEUTRAL_GRAY_200};
            display: flex;
            flex-direction: column;
            z-index: 1000;
            padding: {SPACING_LG};
        }}
        
        /* Sidebar Logo */
        .sidebar-logo {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: {PRIMARY_BLUE};
            margin-bottom: {SPACING_XL};
            text-align: center;
        }}
        
        /* Sidebar Tab Item */
        .sidebar-tab {{
            display: flex;
            align-items: center;
            padding: {SPACING_MD};
            margin-bottom: {SPACING_SM};
            border-left: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: {NEUTRAL_GRAY_700};
            text-decoration: none;
        }}
        
        .sidebar-tab:hover {{
            background-color: {NEUTRAL_GRAY_50};
        }}
        
        .sidebar-tab.active {{
            border-left-color: {PRIMARY_BLUE};
            background-color: {NEUTRAL_GRAY_50};
            color: {PRIMARY_BLUE};
        }}
        
        .sidebar-tab-icon {{
            margin-right: {SPACING_SM};
            font-size: 1.2rem;
        }}
        
        /* Sidebar Version */
        .sidebar-version {{
            margin-top: auto;
            padding-top: {SPACING_LG};
            font-size: 0.75rem;
            color: {NEUTRAL_GRAY_500};
            text-align: center;
            border-top: 1px solid {NEUTRAL_GRAY_200};
        }}
        
        /* Main Content Area */
        .content-area {{
            margin-left: 250px;
            padding: {SPACING_LG};
            min-height: 100vh;
            background-color: {NEUTRAL_GRAY_50};
        }}
        
        /* Cards - white with subtle shadow per design spec */
        .card {{
            background: {NEUTRAL_WHITE};
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            padding: {SPACING_MD};
            margin-bottom: {SPACING_MD};
            transition: opacity 0.3s ease, transform 0.3s ease;
        }}
        
        /* KPI Cards for Dashboard */
        .kpi-card {{
            background: {NEUTRAL_WHITE};
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            padding: {SPACING_LG};
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .kpi-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }}
        
        .kpi-number {{
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: {PRIMARY_BLUE};
            margin-bottom: {SPACING_SM};
        }}
        
        .kpi-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: {NEUTRAL_GRAY_600};
            font-weight: 500;
        }}
        
        /* Call Records List - Gmail-style */
        .call-list-container {{
            background: {NEUTRAL_WHITE};
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }}
        
        .call-item {{
            display: flex;
            align-items: center;
            padding: {SPACING_MD};
            border-bottom: 1px solid {NEUTRAL_GRAY_200};
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .call-item:hover {{
            background-color: {NEUTRAL_GRAY_50};
        }}
        
        .call-item.selected {{
            background-color: {NEUTRAL_GRAY_100};
            border-left: 3px solid {PRIMARY_BLUE};
        }}
        
        .call-id {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            color: {NEUTRAL_GRAY_900};
        }}
        
        .call-subject {{
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: {NEUTRAL_GRAY_700};
            margin-top: 4px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .call-time {{
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: {NEUTRAL_GRAY_500};
            margin-left: auto;
        }}
        
        /* Risk Badges */
        .risk-badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: {SPACING_SM};
        }}
        
        .risk-badge-low {{
            background-color: rgba(34, 197, 94, 0.1);
            color: {RISK_LOW_COLOR};
        }}
        
        .risk-badge-mod {{
            background-color: rgba(250, 204, 21, 0.1);
            color: #d97706;
        }}
        
        .risk-badge-high {{
            background-color: rgba(220, 38, 38, 0.1);
            color: {RISK_HIGH_COLOR};
        }}
        
        .risk-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }}
        
        /* Chat bubbles - kept from original design */
        .chat-bubble {{
            margin: 12px 0;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 75%;
            word-wrap: break-word;
            transition: opacity 0.3s ease;
        }}
        
        .chat-bubble-caller {{
            background: {NEUTRAL_GRAY_100};
            margin-left: 0;
            margin-right: auto;
            border-bottom-left-radius: 4px;
        }}
        
        .chat-bubble-responder {{
            background: {PRIMARY_BLUE};
            color: white;
            margin-left: auto;
            margin-right: 0;
            border-bottom-right-radius: 4px;
        }}
        
        .chat-bubble-speaker {{
            font-weight: bold;
            font-size: 0.85em;
            margin-bottom: 4px;
            opacity: 0.8;
        }}
        
        .chat-bubble-text {{
            line-height: 1.4;
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
        
        /* Alert banner - RED for high risk */
        .alert-banner {{
            background: rgba(220, 38, 38, 0.1);
            color: {RISK_HIGH_COLOR};
            border: 2px solid {RISK_HIGH_COLOR};
            padding: {SPACING_MD};
            margin-bottom: {SPACING_MD};
            border-radius: 8px;
            font-weight: 700;
            text-align: center;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
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
        
        /* Buttons - Rounded pill style */
        .stButton > button {{
            background-color: {PRIMARY_BLUE} !important;
            color: white !important;
            border: none !important;
            border-radius: 24px !important;
            padding: 8px 24px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            background-color: {PRIMARY_BLUE_DARK} !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        }}
        
        .stDownloadButton > button {{
            background-color: {PRIMARY_BLUE} !important;
            color: white !important;
            border: none !important;
            border-radius: 24px !important;
            padding: 8px 24px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: {PRIMARY_BLUE_DARK} !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
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
        
        /* Animations - smooth transitions per design spec */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.3s ease;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .slide-in {{
            animation: slideIn 0.3s ease;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .pulse-animation {{
            animation: pulse 0.6s ease;
        }}
        
        /* Transitions */
        .transition-opacity {{
            transition: opacity 0.3s ease;
        }}
        
        .transition-transform {{
            transition: transform 0.3s ease;
        }}
        
        /* Footer */
        .footer {{
            background: {NEUTRAL_GRAY_100};
            padding: {SPACING_LG};
            margin-top: {SPACING_XXL};
            border-top: 1px solid {NEUTRAL_GRAY_200};
            text-align: center;
            color: {NEUTRAL_GRAY_600};
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
    
    # JavaScript to force sidebar open
    st.markdown("""
    <script>
    // Force sidebar to be open and visible
    window.addEventListener('load', function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.visibility = 'visible';
            sidebar.style.display = 'block';
            sidebar.style.width = '250px';
        }
        
        // Hide collapse button
        const collapseBtn = document.querySelector('button[kind="header"]');
        if (collapseBtn) {
            collapseBtn.style.display = 'none';
        }
    });
    
    // Also run after a short delay to catch dynamic content
    setTimeout(function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.visibility = 'visible';
            sidebar.style.display = 'block';
            sidebar.style.width = '250px';
        }
    }, 100);
    </script>
    """, unsafe_allow_html=True)

def get_risk_color(score: int) -> str:
    """Get color for risk score (0-5)"""
    return RISK_COLORS.get(max(0, min(5, score)), NEUTRAL_GRAY_200)

def get_risk_level(score: int) -> str:
    """Get risk level label (LOW, MOD, HIGH) based on score"""
    if score <= 1:
        return "LOW"
    elif score <= 3:
        return "MOD"
    else:
        return "HIGH"

def get_risk_badge_class(score: int) -> str:
    """Get CSS class for risk badge based on score"""
    if score <= 1:
        return "risk-badge-low"
    elif score <= 3:
        return "risk-badge-mod"
    else:
        return "risk-badge-high"
