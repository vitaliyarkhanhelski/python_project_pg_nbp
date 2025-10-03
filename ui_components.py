#!/usr/bin/env python3
"""
UI Components

This module contains UI component classes for the NBP Streamlit application.
"""

import streamlit as st
import pandas as pd
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
    def render_header(currency=None):
        """Renders the main page header with title and description.
        
        Args:
            currency: The selected currency or asset (changes title and description for Gold)
        """
        st.title(NBPConfig.get_main_title(currency))
        st.markdown(NBPConfig.get_main_description(currency))
    
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
        
        # Initialize default dates in session state if not present
        if 'start_date' not in st.session_state:
            st.session_state.start_date = (datetime.now() - relativedelta(years=1)).date()
        if 'end_date' not in st.session_state:
            st.session_state.end_date = datetime.now().date()
        
        # Set minimum date based on asset type (Gold: 2013, Currencies: 2002)
        year = NBPConfig.MIN_DATE_YEAR_GOLD if currency == NBPConfig.GOLD_ASSET else NBPConfig.MIN_DATE_YEAR_CURRENCIES
        min_date = datetime(year, 1, 2).date()  # Convert to date object for compatibility
        
        # Adjust dates if they're outside the valid range for the selected currency
        if st.session_state.start_date < min_date:
            st.session_state.start_date = min_date
        if st.session_state.end_date < min_date:
            # Set end_date to min_date + 1 year to avoid 0-day range
            end_datetime = datetime.combine(min_date, datetime.min.time()) + relativedelta(years=1)
            st.session_state.end_date = end_datetime.date()
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date_input = st.date_input(
                "Start Date",
                value=st.session_state.start_date,
                min_value=min_date,
                max_value=datetime.now(),
                key="start_date_widget"
            )
            # Update session state with current values
            st.session_state.start_date = start_date_input
            if st.session_state.end_date < st.session_state.start_date:
                st.session_state.end_date = st.session_state.start_date
        with col2:
            end_date_input = st.date_input(
                "End Date",
                value=st.session_state.end_date,
                min_value=st.session_state.start_date,
                max_value=datetime.now(),
                key="end_date_widget"
            )
        # Update session state with current values
        st.session_state.end_date = end_date_input
        
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
    def render_data_table(data, data_label, value_label):
        """Renders the data table with fetched rates/prices.
        
        Args:
            data: Dictionary with date as key and rate/price as value
            data_label: Label for the data type (e.g., "USD Exchange Rates", "Gold Prices")
            value_label: Label for the value column (e.g., "Rate (PLN)", "Price (PLN)")
        """
        st.subheader(f"📈 {data_label} Data")
        
        # Create a DataFrame for better display
        df = pd.DataFrame([
            {"Date": date, value_label: f"{rate:.4f}"}
            for date, rate in data.items()
        ])
        
        # Reset index to start from 1 instead of 0
        df.index = df.index + 1
        
        st.dataframe(df, use_container_width=True)
    
    @staticmethod
    def render_error_message(currency):
        """Renders appropriate error message based on currency type."""
        if currency == NBPConfig.GOLD_ASSET:
            st.error("Failed to fetch gold prices. Please check your date range and try again.")
        else:
            st.error(f"Failed to fetch {currency} exchange rates. Please check your date range and try again.")
