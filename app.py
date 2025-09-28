#!/usr/bin/env python3
"""
NBP Exchange Rate Fetcher

This script fetches USD exchange rates from the Polish National Bank (NBP) API
for a specific date range and returns a dictionary with dates as keys and rates as values.
"""

import requests
import json
from typing import Optional, Dict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetch_usd_exchange_rates() -> Optional[Dict[str, float]]:
    """
    Fetches USD exchange rates from NBP API for date range 2025-09-01 to 2025-09-26
    and returns a dictionary with dates as keys and exchange rates as values.
    
    Returns:
        Dict[str, float]: Dictionary with dates as keys and exchange rates as values, 
                         sorted by date in ascending order, or None if request fails
    """
    url = "https://api.nbp.pl/api/exchangerates/rates/A/USD/2024-09-26/2025-09-26/"
    
    try:
        # Make GET request to NBP API
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
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
            print("Error: No exchange rate data found in response")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request to NBP API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    except KeyError as e:
        print(f"Error: Expected key not found in response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def plot_exchange_rates(exchange_rates: Dict[str, float]) -> None:
    """
    Creates a line chart showing USD exchange rates over time.
    
    Args:
        exchange_rates: Dictionary with dates as keys and exchange rates as values
    """
    if not exchange_rates:
        print("No data to plot")
        return
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in exchange_rates.keys()]
    rates = list(exchange_rates.values())
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(dates, rates, marker='o', linewidth=2, markersize=4)
    
    # Customize the plot
    plt.title('USD Exchange Rate (PLN) - September 2025', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Exchange Rate (PLN)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.xticks(rotation=45)
    
    # Add some styling
    plt.tight_layout()
    
    # Show the plot
    plt.show()


def main():
    """Main function to fetch and display USD exchange rates."""
    print("Fetching USD exchange rates from NBP API for date range 2025-09-01 to 2025-09-26...")
    
    exchange_rates = fetch_usd_exchange_rates()
    
    if exchange_rates is not None:
        print("\nUSD exchange rates (dates in ascending order):")
        print("-" * 50)
        for date, rate in exchange_rates.items():
            print(f"{date}: {rate} zł")
        print(f"\nTotal records: {len(exchange_rates)}")
        
        # Create and display the chart
        print("\nCreating chart...")
        plot_exchange_rates(exchange_rates)
    else:
        print("Failed to fetch exchange rates")


if __name__ == "__main__":
    main()
