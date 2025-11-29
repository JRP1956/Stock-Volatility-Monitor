"""
Core stock monitoring logic
"""
import time
import schedule
from datetime import datetime
from .api_client import StockAPIClient
from .alert_system import AlertSystem
from .stock_config import StockConfig
from .utils import (
    is_market_hours,
    calculate_percentage_change,
    get_timestamp
)


class StockMonitor:
    """Main class for monitoring stock volatility"""

    def __init__(self, config):
        """
        Initialize stock monitor

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api_client = StockAPIClient(config)
        self.stock_config = StockConfig(config)
        self.alert_system = AlertSystem(config, self.stock_config)
        self.is_monitoring = False
        self.check_interval = config.get('check_interval_minutes', 5)

    def add_stock(self, symbol, threshold=None):
        """
        Add a stock to monitor

        Args:
            symbol: Stock symbol (e.g., RELIANCE.NS)
            threshold: Optional custom threshold for this stock

        Returns:
            tuple: (bool, str) - (success, error_message)
        """
        # Validate symbol
        is_valid, error = self.api_client.validate_symbol(symbol)
        if not is_valid:
            return False, error

        # Add to stock config
        self.stock_config.add_stock(symbol.upper(), threshold)
        return True, None

    def remove_stock(self, symbol):
        """
        Remove a stock from monitoring

        Args:
            symbol: Stock symbol

        Returns:
            bool: True if removed successfully
        """
        return self.stock_config.remove_stock(symbol)

    def fetch_opening_prices(self):
        """
        Fetch and store opening prices for all stocks

        Returns:
            tuple: (bool, list) - (all_success, failed_symbols)
        """
        failed_symbols = []
        timestamp = get_timestamp()

        for symbol in self.stock_config.get_all_symbols():
            opening_price, error = self.api_client.get_opening_price(symbol)
            if error:
                self.alert_system.display_error(f"{symbol}: Failed to fetch opening price - {error}")
                failed_symbols.append(symbol)
            else:
                self.stock_config.set_opening_price(symbol, opening_price)
                self.alert_system.display_opening_info(symbol, opening_price, timestamp)

        return len(failed_symbols) == 0, failed_symbols

    def check_price(self):
        """
        Check current prices for all stocks and trigger alerts if needed

        This method is called periodically by the scheduler
        """
        if not self.is_monitoring:
            return

        # Check if we're in market hours
        if not is_market_hours(self.config):
            return

        timestamp = get_timestamp()

        # Check each stock
        for symbol in self.stock_config.get_all_symbols():
            opening_price = self.stock_config.get_opening_price(symbol)
            if not opening_price:
                continue

            # Fetch current price
            current_price, error = self.api_client.get_current_price(symbol)
            if error:
                self.alert_system.display_error(f"{symbol}: Failed to fetch price - {error}")
                continue

            # Calculate percentage change
            percentage_change = calculate_percentage_change(current_price, opening_price)

            # Check if alert should be triggered
            if self.alert_system.should_trigger_alert(symbol, percentage_change):
                self.alert_system.trigger_alert(
                    symbol,
                    current_price,
                    opening_price,
                    percentage_change
                )
            else:
                # Display regular status update
                self.alert_system.display_status(
                    symbol,
                    current_price,
                    opening_price,
                    percentage_change,
                    timestamp
                )

    def start_monitoring(self):
        """
        Start monitoring all added stocks

        Returns:
            tuple: (bool, str) - (success, error_message)
        """
        stock_count = self.stock_config.get_stock_count()
        if stock_count == 0:
            return False, "No stocks added to monitor"

        # Check if market is currently open
        if not is_market_hours(self.config):
            self.alert_system.display_warning(
                "Market is currently closed. Monitoring will start when market opens."
            )

        # Fetch opening prices for all stocks
        success, failed_symbols = self.fetch_opening_prices()
        if failed_symbols:
            self.alert_system.display_warning(
                f"Failed to fetch opening prices for: {', '.join(failed_symbols)}"
            )

        # Set monitoring flag
        self.is_monitoring = True

        # Display monitoring info
        self.alert_system.display_info(f"\nMonitoring {stock_count} stock(s)")
        for symbol in self.stock_config.get_all_symbols():
            threshold = self.stock_config.get_threshold(symbol)
            self.alert_system.display_info(f"  - {symbol} (threshold: {threshold}%)")

        self.alert_system.display_info(
            f"\nChecking every {self.check_interval} minutes during market hours (09:15 - 15:30 IST)"
        )
        self.alert_system.display_info("Press Ctrl+C to stop monitoring\n")

        # Schedule periodic checks
        schedule.every(self.check_interval).minutes.do(self.check_price)

        # Run the monitoring loop
        try:
            while self.is_monitoring:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()

        return True, None

    def stop_monitoring(self):
        """Stop monitoring all stocks"""
        self.is_monitoring = False
        schedule.clear()

        # Display final info for all stocks
        timestamp = get_timestamp()
        for symbol in self.stock_config.get_all_symbols():
            opening_price = self.stock_config.get_opening_price(symbol)
            if opening_price:
                current_price, error = self.api_client.get_current_price(symbol)
                if not error and current_price:
                    percentage_change = calculate_percentage_change(current_price, opening_price)
                    self.alert_system.display_closing_info(
                        symbol,
                        current_price,
                        opening_price,
                        percentage_change,
                        timestamp
                    )

        self.alert_system.display_info("\nMonitoring stopped.")

    def get_current_status(self):
        """
        Get current monitoring status for all stocks

        Returns:
            dict: Status information
        """
        if not self.is_monitoring:
            return {'monitoring': False}

        stocks_status = {}
        for symbol in self.stock_config.get_all_symbols():
            opening_price = self.stock_config.get_opening_price(symbol)
            if not opening_price:
                stocks_status[symbol] = {'error': 'No opening price'}
                continue

            current_price, error = self.api_client.get_current_price(symbol)
            if error:
                stocks_status[symbol] = {'error': error}
                continue

            percentage_change = calculate_percentage_change(current_price, opening_price)
            stocks_status[symbol] = {
                'opening_price': opening_price,
                'current_price': current_price,
                'percentage_change': percentage_change,
                'threshold': self.stock_config.get_threshold(symbol)
            }

        return {
            'monitoring': True,
            'stock_count': self.stock_config.get_stock_count(),
            'stocks': stocks_status,
            'in_market_hours': is_market_hours(self.config)
        }

    def get_monitored_stocks(self):
        """
        Get list of all monitored stock symbols

        Returns:
            list: List of stock symbols
        """
        return self.stock_config.get_all_symbols()
