#!/usr/bin/env python3
"""
NBP Exchange Rate Streamlit App

Interactive web application for fetching and visualizing exchange rates
from the Polish National Bank (NBP) API.
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetch_gold_prices(start_date: str, end_date: str) -> Optional[Dict[str, float]]:
    """
    Fetches gold prices from NBP API for specified date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dict[str, float]: Dictionary with dates as keys and gold prices as values, 
                         sorted by date in ascending order, or None if request fails
    """
    url = f"https://api.nbp.pl/api/cenyzlota/{start_date}/{end_date}/"
    
    try:
        # Make GET request to NBP API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract gold prices and create dictionary
        if len(data) > 0:
            gold_prices = {}
            for item in data:
                date = item['data']
                price = item['cena']
                gold_prices[date] = price
            
            # Sort dictionary by date (ascending order)
            sorted_prices = dict(sorted(gold_prices.items()))
            return sorted_prices
        else:
            st.error("No gold price data found in response")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to NBP API: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {e}")
        return None
    except KeyError as e:
        st.error(f"Error: Expected key not found in response: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


def fetch_exchange_rates(currency: str, start_date: str, end_date: str) -> Optional[Dict[str, float]]:
    """
    Fetches exchange rates from NBP API for specified currency and date range.
    
    Args:
        currency: Currency code (USD, EUR, etc.)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dict[str, float]: Dictionary with dates as keys and exchange rates as values, 
                         sorted by date in ascending order, or None if request fails
    """
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date}/{end_date}/"
    
    try:
        # Make GET request to NBP API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract exchange rates and create dictionary
        if 'rates' in data and len(data['rates']) > 0:
            exchange_rates = {}
            for rate in data['rates']:
                effective_date = rate['effectiveDate']
                mid_rate = rate['mid']
                exchange_rates[effective_date] = mid_rate
            
            # Sort dictionary by date (ascending order)
            sorted_rates = dict(sorted(exchange_rates.items()))
            return sorted_rates
        else:
            st.error("No exchange rate data found in response")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to NBP API: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {e}")
        return None
    except KeyError as e:
        st.error(f"Error: Expected key not found in response: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


def create_exchange_rate_chart(data: Dict[str, float], data_type: str, currency: str = None) -> None:
    """
    Creates a line chart showing exchange rates or gold prices over time.
    
    Args:
        data: Dictionary with dates as keys and rates/prices as values
        data_type: Type of data ('exchange_rate' or 'gold_price')
        currency: Currency code for the title (only for exchange rates)
    """
    if not data:
        st.warning("No data to plot")
        return
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in data.keys()]
    values = list(data.values())
    
    # Create the plot with transparent background
    fig, ax = plt.subplots(figsize=(12, 6))
    # fig.patch.set_facecolor('none')  # Make figure background transparent
    # ax.set_facecolor('none')  # Make axes background transparent
    
    ax.plot(dates, values, marker='o', linewidth=2, markersize=4, color='#1f77b4')
    
    # Customize the plot based on data type
    if data_type == 'gold_price':
        ax.set_title(f'Gold Price, PLN ({dates[0].strftime("%b %Y")} - {dates[-1].strftime("%b %Y")})', 
                     fontsize=14, fontweight='bold')
        ax.set_ylabel('Price (PLN)', fontsize=12)
    else:  # exchange_rate
        ax.set_title(f'{currency} Exchange Rate, PLN ({dates[0].strftime("%b %Y")} - {dates[-1].strftime("%b %Y")})', 
                     fontsize=14, fontweight='bold')
        ax.set_ylabel('Exchange Rate (PLN)', fontsize=12)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Format x-axis to show dates nicely
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Add some styling
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig, transparent=True)


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="NBP Exchange Rates",
        page_icon="💰",
        layout="wide"
    )
    
    # Add modern background
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
    
    # Title and description
    st.title("💰 NBP Exchange Rates Dashboard")
    st.markdown("Fetch and visualize exchange rates from the Polish National Bank (NBP) API")
    
    # Sidebar for controls
    st.sidebar.header("Settings")
    
    # Currency selection
    currency = st.sidebar.selectbox(
        "Select Currency/Asset",
        ["USD", "EUR", "CHF", "GBP", "Gold"],
        help="Choose the currency to fetch exchange rates for or Gold for gold prices"
    )
    
    # Date range selection
    st.sidebar.subheader("Date Range")
    
    # Set default to last 30 days, but allow going back to 2002
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Set minimum date to 2002 (when NBP data starts)
    min_date = datetime(2002, 1, 1)
    
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
    
    # Convert dates to string format
    start_date_str = start_date_input.strftime('%Y-%m-%d')
    end_date_str = end_date_input.strftime('%Y-%m-%d')
    
    # Calculate date range in days
    date_range_days = (end_date_input - start_date_input).days
    
    # Validate date range (max 367 days)
    is_valid_range = date_range_days <= 367
    
    # Show validation message
    if not is_valid_range:
        st.sidebar.error(f"❌ Date range too large! Maximum 367 days allowed. Current range: {date_range_days} days")
    else:
        st.sidebar.success(f"✅ Date range: {date_range_days} days")
    
    # Fetch button (disabled if invalid range)
    if st.sidebar.button("📊 Fetch Data", type="primary", disabled=not is_valid_range):
        if currency == "Gold":
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
            import pandas as pd
            df = pd.DataFrame([
                {"Date": date, value_label: f"{rate:.4f}"}
                for date, rate in data.items()
            ])
            
            # Reset index to start from 1 instead of 0
            df.index = df.index + 1
            
            st.dataframe(df, use_container_width=True)

            # Display statistics
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
            
            # Create and display the chart
            st.subheader("📊 Chart")
            create_exchange_rate_chart(data, data_type, currency)
            
        else:
            st.error("Failed to fetch data. Please check your date range and try again.")
    
    # Instructions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("""
    1. Select a currency (USD, EUR, CHF, GBP) or Gold
    2. Choose your date range (max 367 days)
    3. Click "Fetch Data"
    4. View the data table and chart
    """)
    
    st.sidebar.markdown("### API Limits")
    st.sidebar.markdown("""
    - Maximum date range: **367 days**
    - Data available from 2002
    - Weekends and holidays excluded
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("Data source: [NBP API](https://api.nbp.pl/)")


if __name__ == "__main__":
    main()
