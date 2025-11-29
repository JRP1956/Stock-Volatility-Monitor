"""
API Client for fetching stock data using yfinance
"""
import yfinance as yf
import time
from datetime import datetime


class StockAPIClient:
    """Client for interacting with Yahoo Finance API"""

    def __init__(self, config):
        """
        Initialize API client

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.retry_attempts = config.get('api_retry_attempts', 3)
        self.timeout = config.get('api_timeout_seconds', 5)

    def validate_symbol(self, symbol):
        """
        Validate if stock symbol exists

        Args:
            symbol: Stock symbol (e.g., RELIANCE.NS)

        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Check if we got valid data
            if not info or 'symbol' not in info:
                return False, f"Invalid stock symbol: {symbol}"

            return True, None

        except Exception as e:
            return False, f"Error validating symbol: {str(e)}"

    def get_opening_price(self, symbol):
        """
        Get today's opening price for a stock

        Args:
            symbol: Stock symbol

        Returns:
            tuple: (float, str) - (opening_price, error_message)
        """
        for attempt in range(self.retry_attempts):
            try:
                ticker = yf.Ticker(symbol)
                # Get today's data
                hist = ticker.history(period="1d", interval="1d")

                if hist.empty:
                    return None, "No data available for today"

                opening_price = hist['Open'].iloc[-1]
                return float(opening_price), None

            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    time.sleep(1)
                    continue
                return None, f"Error fetching opening price: {str(e)}"

        return None, "Failed to fetch opening price after multiple attempts"

    def get_current_price(self, symbol):
        """
        Get current price for a stock

        Args:
            symbol: Stock symbol

        Returns:
            tuple: (float, str) - (current_price, error_message)
        """
        for attempt in range(self.retry_attempts):
            try:
                ticker = yf.Ticker(symbol)

                # Try to get current price from info
                info = ticker.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')

                if current_price:
                    return float(current_price), None

                # Fallback: Get latest price from history
                hist = ticker.history(period="1d", interval="1m")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    return float(current_price), None

                return None, "No current price data available"

            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    time.sleep(1)
                    continue
                return None, f"Error fetching current price: {str(e)}"

        return None, "Failed to fetch current price after multiple attempts"

    def get_stock_info(self, symbol):
        """
        Get basic stock information

        Args:
            symbol: Stock symbol

        Returns:
            tuple: (dict, str) - (stock_info, error_message)
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            stock_info = {
                'symbol': info.get('symbol', symbol),
                'name': info.get('longName', 'N/A'),
                'currency': info.get('currency', 'INR'),
                'exchange': info.get('exchange', 'NSE')
            }

            return stock_info, None

        except Exception as e:
            return None, f"Error fetching stock info: {str(e)}"

    def get_opening_and_current_price(self, symbol):
        """
        Get both opening and current price in one call

        Args:
            symbol: Stock symbol

        Returns:
            tuple: (dict, str) - (prices_dict, error_message)
        """
        opening_price, open_error = self.get_opening_price(symbol)
        if open_error:
            return None, open_error

        current_price, current_error = self.get_current_price(symbol)
        if current_error:
            return None, current_error

        return {
            'opening_price': opening_price,
            'current_price': current_price
        }, None
