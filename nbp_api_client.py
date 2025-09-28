#!/usr/bin/env python3
"""
NBP API Client

This module contains functions for fetching data from the Polish National Bank (NBP) API.
It acts as a client to invoke NBP API endpoints for exchange rates and gold prices.
"""

import requests
import json
from typing import Optional, Dict
from config import NBPConfig


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
    url = f"{NBPConfig.GOLD_PRICES_BASE_URL}/{start_date}/{end_date}/"
    
    try:
        # Make GET request to NBP API
        response = requests.get(url, timeout=NBPConfig.REQUEST_TIMEOUT)
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
            return None
            
    except requests.exceptions.RequestException as e:
        return None
    except json.JSONDecodeError as e:
        return None
    except KeyError as e:
        return None
    except Exception as e:
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
    url = f"{NBPConfig.EXCHANGE_RATES_BASE_URL}/{currency}/{start_date}/{end_date}/"
    
    try:
        # Make GET request to NBP API
        response = requests.get(url, timeout=NBPConfig.REQUEST_TIMEOUT)
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
            return None
            
    except requests.exceptions.RequestException as e:
        return None
    except json.JSONDecodeError as e:
        return None
    except KeyError as e:
        return None
    except Exception as e:
        return None
