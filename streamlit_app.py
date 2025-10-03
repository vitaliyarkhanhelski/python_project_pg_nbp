#!/usr/bin/env python3
"""
NBP Exchange Rate Streamlit App

Interactive web application for fetching and visualizing exchange rates
from the Polish National Bank (NBP) API.

Author: Vitaliy Arkhanhelski
Created: 2025-09-28
"""

import streamlit as st
from nbp_api_client import fetch_gold_prices, fetch_exchange_rates
from config import NBPConfig
from chart_utils import ChartRenderer
from css_utils import CSSRenderer
from ui_components import UIRenderer
import time

def main():
    # Setup page configuration and styling
    # Initialize session state for auto-fetch behavior
    if 'fetch' not in st.session_state:
        st.session_state.fetch = False
    if 'prev_dates' not in st.session_state:
        st.session_state.prev_dates = None

    UIRenderer.setup_page()
    CSSRenderer.apply_custom_styles()
    
    # Render sidebar controls
    UIRenderer.render_sidebar_header()
    currency = UIRenderer.render_currency_selection()
    
    # Render main page header with dynamic description
    UIRenderer.render_header(currency)
    
    # Apply dynamic background based on currency selection
    CSSRenderer.apply_background(currency)
    
    start_date_input, end_date_input = UIRenderer.render_date_range_section(currency)
    
    # Convert dates to string format
    start_date_str = start_date_input.strftime('%Y-%m-%d')
    end_date_str = end_date_input.strftime('%Y-%m-%d')
    
    # Calculate date range in days
    date_range_days = (end_date_input - start_date_input).days
    
    # Validate date range and render validation messages
    is_valid_range = UIRenderer.render_date_validation(date_range_days)
    
    # Check if dates have changed
    current_dates = (start_date_str, end_date_str)
    if st.session_state.prev_dates is not None and st.session_state.prev_dates != current_dates:
        st.session_state.fetch = False
    
    # Render fetch button
    fetch_button_clicked = UIRenderer.render_fetch_button()
    
    # Set flag on button click
    if fetch_button_clicked:
        st.session_state.fetch = True
        st.session_state.prev_dates = current_dates
    
    # Fetch data if: button was clicked OR flag is True (auto-fetch after first time)
    if (fetch_button_clicked or st.session_state.fetch) and is_valid_range:
        # Determine spinner message based on currency
        spinner_message = f"Fetching and visualizing {'gold prices' if currency == NBPConfig.GOLD_ASSET else f'{currency} exchange rates'}..."
        
        # Initialize data variable
        data = None
        
        with st.spinner(spinner_message):
            # Fetch data
            if currency == NBPConfig.GOLD_ASSET:
                data = fetch_gold_prices(start_date_str, end_date_str)
                data_type = "gold_price"
                data_label = "Gold Prices"
                value_label = "Price (PLN)"
            else:
                data = fetch_exchange_rates(currency, start_date_str, end_date_str)
                data_type = "exchange_rate"
                data_label = f"{currency} Exchange Rates"
                value_label = "Rate (PLN)"
            
            if data:
                # Set flag and store current dates for auto-fetch on currency change
                st.session_state.fetch = True
                st.session_state.prev_dates = (start_date_str, end_date_str)
                
                # Display data in a table
                UIRenderer.render_data_table(data, data_label, value_label)

                # Display statistics
                UIRenderer.render_statistics(data)
                
                # Create and display the chart
                ChartRenderer.create_exchange_rate_chart(data, data_type, currency)
                
                # Add small delay to ensure chart is fully created
        
        # Show success or error message after spinner completes
        if data:
            st.success(f"Successfully fetched {len(data)} {data_label.lower()} records!")
        else:
            UIRenderer.render_error_message(currency)
    
    # Render sidebar information and footer
    UIRenderer.render_sidebar_info()
    UIRenderer.render_footer()


if __name__ == "__main__":
    main()
