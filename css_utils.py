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
        /* Main app background */
        .stApp {
            background: linear-gradient(to bottom, #ffffff, #c2d6f0);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #2c3e50, #34495e);
        }
        
        /* Sidebar text - set all text to light color */
        [data-testid="stSidebar"] * {
            color: #ecf0f1 !important;
        }
        
        /* Input fields - override with dark text for readability */
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] .stSelectbox > div > div > div,
        [data-testid="stSidebar"] .stDateInput > div > div > div,
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] *,
        [data-testid="stSidebar"] .stDateInput [data-baseweb="select"] * {
            color: #2c3e50 !important;
        }
        
        /* Main content area styling */
        .main .block-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
