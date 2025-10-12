"""
Simple test to check if Streamlit works without Plotly
"""
import os
import sys

# Disable Plotly to avoid compatibility issues
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

try:
    import streamlit as st
    print("✅ Streamlit import successful!")
    
    # Test basic Streamlit functionality
    st.title("EmpathZ AI Coordinator Demo")
    st.write("This is a test to verify Streamlit is working.")
    
    if st.button("Test Button"):
        st.success("Button works!")
        
    print("✅ Streamlit test completed successfully!")
    
except Exception as e:
    print(f"❌ Streamlit test failed: {e}")
    import traceback
    traceback.print_exc()
