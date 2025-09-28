#!/usr/bin/env python3
"""
CSS Utilities

This module contains CSS styling utilities for the NBP Streamlit application.
"""

import streamlit as st


class CSSRenderer:
    """Class for rendering CSS styles and themes."""
    
    @staticmethod
    def apply_custom_styles():
        """Applies custom CSS styles to the Streamlit application."""
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #ffffff, #c2d6f0);
        }
        
        .sidebar .sidebar-content {
            background: #d1884f !important;
            border-radius: 15px;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #2c3e50, #34495e);
            color: #ecf0f1;
        }
        
        [data-testid="stSidebar"] * {
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] label {
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stDateInput label {
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] .stText {
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] div[data-testid="stSelectbox"] label,
        [data-testid="stSidebar"] div[data-testid="stDateInput"] label {
            color: #ecf0f1 !important;
        }
        
        /* Fix input field text color - make it dark for readability */
        [data-testid="stSidebar"] .stSelectbox > div > div > div {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stDateInput > div > div > div {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] input {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox input {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stDateInput input {
            color: #2c3e50 !important;
        }
        
        /* Additional selectbox text targeting */
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
            color: #2c3e50 !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
            color: #2c3e50 !important;
        }
        
        .main .block-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
