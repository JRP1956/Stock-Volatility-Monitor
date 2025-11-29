"""
Utility functions for Stock Volatility Monitor
"""
import yaml
from datetime import datetime, time
import pytz
from pathlib import Path


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        return None


def is_market_hours(config):
    """
    Check if current time is within market hours

    Args:
        config: Configuration dictionary

    Returns:
        bool: True if within market hours, False otherwise
    """
    tz = pytz.timezone(config.get('timezone', 'Asia/Kolkata'))
    now = datetime.now(tz)

    # Get market open and close times
    open_time_str = config.get('market_open_time', '09:15')
    close_time_str = config.get('market_close_time', '15:30')

    # Parse times
    open_hour, open_minute = map(int, open_time_str.split(':'))
    close_hour, close_minute = map(int, close_time_str.split(':'))

    market_open = time(open_hour, open_minute)
    market_close = time(close_hour, close_minute)

    current_time = now.time()

    # Check if it's a weekday (Monday=0, Sunday=6)
    is_weekday = now.weekday() < 5

    return is_weekday and market_open <= current_time <= market_close


def format_currency(amount):
    """
    Format amount as Indian Rupees

    Args:
        amount: Float value to format

    Returns:
        str: Formatted currency string
    """
    return f"₹{amount:,.2f}"


def calculate_percentage_change(current_price, open_price):
    """
    Calculate percentage change from open price

    Args:
        current_price: Current stock price
        open_price: Opening price

    Returns:
        float: Percentage change
    """
    if open_price == 0:
        return 0.0
    return ((current_price - open_price) / open_price) * 100


def validate_stock_symbol(symbol):
    """
    Validate stock symbol format

    Args:
        symbol: Stock symbol string

    Returns:
        bool: True if valid format, False otherwise
    """
    if not symbol:
        return False

    # Check if it ends with .NS or .BO
    return symbol.endswith('.NS') or symbol.endswith('.BO')


def get_timestamp():
    """
    Get current timestamp in IST

    Returns:
        str: Formatted timestamp
    """
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S")


def get_full_timestamp():
    """
    Get full timestamp with date and time

    Returns:
        str: Formatted full timestamp
    """
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")
