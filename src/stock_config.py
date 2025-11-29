"""
Stock configuration management for per-stock settings
"""


class StockConfig:
    """Manages stock-specific configuration"""

    def __init__(self, config):
        """
        Initialize stock configuration manager

        Args:
            config: Global configuration dictionary
        """
        self.global_config = config
        self.default_threshold = config.get('threshold_percent', 5.0)
        self.stock_thresholds = config.get('stock_thresholds', {})
        self.stocks = {}

    def add_stock(self, symbol, threshold=None):
        """
        Add a stock to monitor with optional custom threshold

        Args:
            symbol: Stock symbol (e.g., TCS.NS)
            threshold: Custom threshold percentage (optional)

        Returns:
            bool: True if added successfully
        """
        symbol = symbol.upper()

        # Use custom threshold if provided, otherwise check config, then use default
        if threshold is not None:
            stock_threshold = threshold
        else:
            stock_threshold = self.stock_thresholds.get(symbol, self.default_threshold)

        self.stocks[symbol] = {
            'threshold': stock_threshold,
            'opening_price': None,
            'last_alert_time': None
        }

        return True

    def remove_stock(self, symbol):
        """
        Remove a stock from monitoring

        Args:
            symbol: Stock symbol

        Returns:
            bool: True if removed successfully
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            del self.stocks[symbol]
            return True
        return False

    def get_threshold(self, symbol):
        """
        Get threshold for a specific stock

        Args:
            symbol: Stock symbol

        Returns:
            float: Threshold percentage
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            return self.stocks[symbol]['threshold']
        return self.default_threshold

    def set_opening_price(self, symbol, opening_price):
        """
        Set opening price for a stock

        Args:
            symbol: Stock symbol
            opening_price: Opening price value
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            self.stocks[symbol]['opening_price'] = opening_price

    def get_opening_price(self, symbol):
        """
        Get opening price for a stock

        Args:
            symbol: Stock symbol

        Returns:
            float: Opening price or None
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            return self.stocks[symbol]['opening_price']
        return None

    def set_last_alert_time(self, symbol, alert_time):
        """
        Set last alert time for a stock

        Args:
            symbol: Stock symbol
            alert_time: DateTime of last alert
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            self.stocks[symbol]['last_alert_time'] = alert_time

    def get_last_alert_time(self, symbol):
        """
        Get last alert time for a stock

        Args:
            symbol: Stock symbol

        Returns:
            datetime: Last alert time or None
        """
        symbol = symbol.upper()
        if symbol in self.stocks:
            return self.stocks[symbol]['last_alert_time']
        return None

    def get_all_symbols(self):
        """
        Get all monitored stock symbols

        Returns:
            list: List of stock symbols
        """
        return list(self.stocks.keys())

    def get_stock_count(self):
        """
        Get number of stocks being monitored

        Returns:
            int: Number of stocks
        """
        return len(self.stocks)

    def get_stock_info(self, symbol):
        """
        Get all info for a specific stock

        Args:
            symbol: Stock symbol

        Returns:
            dict: Stock information or None
        """
        symbol = symbol.upper()
        return self.stocks.get(symbol)

    def get_all_stocks_info(self):
        """
        Get information for all stocks

        Returns:
            dict: Dictionary of all stock information
        """
        return self.stocks.copy()
