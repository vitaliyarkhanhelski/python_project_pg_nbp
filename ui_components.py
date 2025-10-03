#!/usr/bin/env python3
"""
UI Components

This module contains UI component classes for the NBP Streamlit application.
"""

import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import NBPConfig


class UIRenderer:
    """Class for rendering UI components and layouts."""
    
    @staticmethod
    def setup_page():
        """Sets up the page configuration and basic layout."""
        st.set_page_config(
            page_title=NBPConfig.PAGE_TITLE,
            page_icon="💰",
            layout="wide"
        )
    
    @staticmethod
    def render_header():
        """Renders the main page header with title and description."""
        st.title(NBPConfig.MAIN_TITLE)
        st.markdown(NBPConfig.MAIN_DESCRIPTION)
    
    @staticmethod
    def render_sidebar_header():
        """Renders the sidebar header."""
        st.sidebar.header("Settings")
    
    @staticmethod
    def render_currency_selection():
        """Renders the currency selection dropdown and returns the selected currency."""
        return st.sidebar.selectbox(
            "Select Currency/Asset",
            NBPConfig.SUPPORTED_CURRENCIES + [NBPConfig.GOLD_ASSET],
            help="Choose the currency to fetch exchange rates for or Gold for gold prices"
        )
    
    @staticmethod
    def render_date_range_section(currency):
        """Renders the date range selection section and returns the selected dates.
        
        Args:
            currency: The selected currency or asset (e.g., 'USD', 'EUR', 'Gold')
        """
        st.sidebar.subheader("Date Range")
        
        # Set default to last 1 year (accounts for leap years)
        end_date = datetime.now()
        start_date = end_date - relativedelta(years=1)
        
        # Set minimum date based on asset type (Gold: 2013, Currencies: 2002)
        year = NBPConfig.MIN_DATE_YEAR_GOLD if currency == NBPConfig.GOLD_ASSET else NBPConfig.MIN_DATE_YEAR_CURRENCIES
        min_date = datetime(year, 1, 2)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date_input = st.date_input(
                "Start Date",
                value=start_date,
                min_value=min_date,
                max_value=end_date
            )
        with col2:
            end_date_input = st.date_input(
                "End Date",
                value=end_date,
                min_value=min_date,
                max_value=datetime.now()
            )
        
        return start_date_input, end_date_input
    
    @staticmethod
    def render_date_validation(date_range_days):
        """Renders date range validation messages."""
        is_valid_range = date_range_days <= NBPConfig.MAX_DATE_RANGE_DAYS
        
        if not is_valid_range:
            st.sidebar.error(f"❌ Date range too large! Maximum {NBPConfig.MAX_DATE_RANGE_DAYS} days allowed. Current range: {date_range_days} days")
        else:
            st.sidebar.success(f"✅ Date range: {date_range_days} days")
        
        return is_valid_range
    
    @staticmethod
    def render_fetch_button():
        """Renders the fetch data button and returns the button state."""
        return st.sidebar.button("📊 Fetch Data", type="primary")
    
    @staticmethod
    def render_sidebar_info():
        """Renders the sidebar instructions and API limits."""
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Instructions")
        st.sidebar.markdown(NBPConfig.SIDEBAR_INSTRUCTIONS)
        
        st.sidebar.markdown("### API Limits")
        st.sidebar.markdown(NBPConfig.API_LIMITS)
    
    @staticmethod
    def render_footer():
        """Renders the page footer."""
        st.markdown("---")
        st.markdown(NBPConfig.FOOTER_MESSAGE)
    
    @staticmethod
    def render_statistics(data):
        """Renders statistics metrics for the data."""
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Records", len(data))
        with col2:
            st.metric("Min Value", f"{round(min(data.values()), 4)} PLN")
        with col3:
            st.metric("Max Value", f"{round(max(data.values()), 4)} PLN")
        with col4:
            avg_value = sum(data.values()) / len(data)
            st.metric("Avg Value", f"{avg_value:.4f} PLN")
    
    @staticmethod
    def render_error_message(currency):
        """Renders appropriate error message based on currency type."""
        if currency == NBPConfig.GOLD_ASSET:
            st.error("Failed to fetch gold prices. Please check your date range and try again.")
        else:
            st.error(f"Failed to fetch {currency} exchange rates. Please check your date range and try again.")
