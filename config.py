#!/usr/bin/env python3
"""
Configuration Constants

This module contains configuration constants for the NBP API client and application.
"""


class NBPConfig:
    """Configuration constants for NBP API and application settings."""
    
    # NBP API Base URL
    API_BASE_URL = "https://api.nbp.pl"
    
    # NBP API Endpoints
    EXCHANGE_RATES_BASE_URL = f"{API_BASE_URL}/api/exchangerates/rates/A"
    GOLD_PRICES_BASE_URL = f"{API_BASE_URL}/api/cenyzlota"
    
    # API Settings
    REQUEST_TIMEOUT = 10
    
    # Date Range Limits
    MAX_DATE_RANGE_DAYS = 367
    MIN_DATE_YEAR_CURRENCIES = 2002  # Currency exchange rates start from Jan 2, 2002
    MIN_DATE_YEAR_GOLD = 2013  # Gold prices start from Jan 2, 2013
    
    # Supported Currencies
    SUPPORTED_CURRENCIES = ["USD", "EUR", "CHF", "GBP"]
    GOLD_ASSET = "Gold"
    
    # UI Messages
    PAGE_TITLE = "NBP Exchange Rates"
    FOOTER_MESSAGE = f"Data source: [NBP API]({API_BASE_URL})"
    SIDEBAR_INSTRUCTIONS = f"""
    1. Select a currency ({', '.join(SUPPORTED_CURRENCIES)}) or {GOLD_ASSET}
    2. Choose your date range (max {MAX_DATE_RANGE_DAYS} days)
    3. Click "Fetch Data"
    4. View the data table and chart
    """
    API_LIMITS = f"""
    - Maximum date range: **{MAX_DATE_RANGE_DAYS} days**
    - Currency data from **{MIN_DATE_YEAR_CURRENCIES}**
    - Gold data from **{MIN_DATE_YEAR_GOLD}**
    - Weekends and holidays excluded
    """
    
    @classmethod
    def get_main_title(cls, currency):
        """Returns the appropriate main title based on currency selection.
        
        Args:
            currency: The selected currency or asset (e.g., 'USD', 'EUR', 'Gold')
            
        Returns:
            str: Title for the main header
        """
        return f"💰 NBP {'Gold Prices' if currency == cls.GOLD_ASSET else 'Exchange Rates'} Dashboard"
    
    @classmethod
    def get_main_description(cls, currency):
        """Returns the appropriate main description based on currency selection.
        
        Args:
            currency: The selected currency or asset (e.g., 'USD', 'EUR', 'Gold')
            
        Returns:
            str: Description message for the main header
        """
        return f"Fetch and visualize {'gold prices' if currency == cls.GOLD_ASSET else 'exchange rates'} from the Polish National Bank (NBP) API"
    
