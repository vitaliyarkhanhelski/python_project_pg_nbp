#!/usr/bin/env python3
"""
NBP Exchange Rate Streamlit App

Interactive web application for fetching and visualizing exchange rates
from the Polish National Bank (NBP) API.

Author: Vitaliy Arkhanhelskiy
Created: 2025-09-28
"""

import streamlit as st
import pandas as pd
from nbp_api_client import fetch_gold_prices, fetch_exchange_rates
from config import NBPConfig
from chart_utils import ChartRenderer
from css_utils import CSSRenderer
from ui_components import UIRenderer


def main():
    # Setup page configuration and styling
    UIRenderer.setup_page()
    CSSRenderer.apply_custom_styles()
    
    # Render main page header
    UIRenderer.render_header()
    
    # Render sidebar controls
    UIRenderer.render_sidebar_header()
    currency = UIRenderer.render_currency_selection()
    start_date_input, end_date_input = UIRenderer.render_date_range_section()
    
    # Convert dates to string format
    start_date_str = start_date_input.strftime('%Y-%m-%d')
    end_date_str = end_date_input.strftime('%Y-%m-%d')
    
    # Calculate date range in days
    date_range_days = (end_date_input - start_date_input).days
    
    # Validate date range and render validation messages
    is_valid_range = UIRenderer.render_date_validation(date_range_days)
    
    # Render fetch button and handle data fetching
    if UIRenderer.render_fetch_button() and is_valid_range:
        if currency == NBPConfig.GOLD_ASSET:
            with st.spinner(f"Fetching gold prices..."):
                data = fetch_gold_prices(start_date_str, end_date_str)
                data_type = "gold_price"
                data_label = "Gold Prices"
                value_label = "Price (PLN)"
        else:
            with st.spinner(f"Fetching {currency} exchange rates..."):
                data = fetch_exchange_rates(currency, start_date_str, end_date_str)
                data_type = "exchange_rate"
                data_label = f"{currency} Exchange Rates"
                value_label = "Rate (PLN)"
        
        if data:
            st.success(f"Successfully fetched {len(data)} {data_label.lower()} records!")
            
            # Display data in a table
            st.subheader(f"📈 {data_label} Data")
            
            # Create a DataFrame for better display
            df = pd.DataFrame([
                {"Date": date, value_label: f"{rate:.4f}"}
                for date, rate in data.items()
            ])
            
            # Reset index to start from 1 instead of 0
            df.index = df.index + 1
            
            st.dataframe(df, use_container_width=True)

            # Display statistics
            UIRenderer.render_statistics(data)
            
            # Create and display the chart
            ChartRenderer.create_exchange_rate_chart(data, data_type, currency)
        else:
            UIRenderer.render_error_message(currency)
    
    # Render sidebar information and footer
    UIRenderer.render_sidebar_info()
    UIRenderer.render_footer()


if __name__ == "__main__":
    main()
