#!/usr/bin/env python3
"""
Chart Utilities

This module contains chart creation and visualization utilities for the NBP application.
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict
from datetime import datetime


class ChartRenderer:
    """Class for rendering charts and visualizations."""
    
    @staticmethod
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
        
        # Render chart subheader
        st.subheader("📊 Chart")
        
        # Convert string dates to datetime objects
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in data.keys()]
        values = list(data.values())
        
        # Create the plot with transparent background
        fig, ax = plt.subplots(figsize=(12, 6))
        
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
