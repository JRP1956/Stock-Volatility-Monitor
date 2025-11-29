"""
Core stock monitoring logic
"""
import time
import schedule
from datetime import datetime
from .api_client import StockAPIClient
from .alert_system import AlertSystem
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
        self.alert_system = AlertSystem(config)
        self.symbol = None
        self.opening_price = None
        self.is_monitoring = False
        self.check_interval = config.get('check_interval_minutes', 5)

    def set_stock(self, symbol):
        """
        Set the stock symbol to monitor

        Args:
            symbol: Stock symbol (e.g., RELIANCE.NS)

        Returns:
            tuple: (bool, str) - (success, error_message)
        """
        # Validate symbol
        is_valid, error = self.api_client.validate_symbol(symbol)
        if not is_valid:
            return False, error

        self.symbol = symbol.upper()
        return True, None

    def fetch_opening_price(self):
        """
        Fetch and store the opening price

        Returns:
            tuple: (bool, str) - (success, error_message)
        """
        opening_price, error = self.api_client.get_opening_price(self.symbol)
        if error:
            return False, error

        self.opening_price = opening_price
        timestamp = get_timestamp()
        self.alert_system.display_opening_info(self.symbol, self.opening_price, timestamp)
        return True, None

    def check_price(self):
        """
        Check current price and trigger alerts if needed

        This method is called periodically by the scheduler
        """
        if not self.is_monitoring:
            return

        # Check if we're in market hours
        if not is_market_hours(self.config):
            return

        # Fetch current price
        current_price, error = self.api_client.get_current_price(self.symbol)
        if error:
            self.alert_system.display_error(f"Failed to fetch price: {error}")
            return

        # Calculate percentage change
        percentage_change = calculate_percentage_change(current_price, self.opening_price)

        # Get timestamp
        timestamp = get_timestamp()

        # Check if alert should be triggered
        if self.alert_system.should_trigger_alert(self.symbol, percentage_change):
            self.alert_system.trigger_alert(
                self.symbol,
                current_price,
                self.opening_price,
                percentage_change
            )
        else:
            # Display regular status update
            self.alert_system.display_status(
                self.symbol,
                current_price,
                self.opening_price,
                percentage_change,
                timestamp
            )

    def start_monitoring(self):
        """
        Start monitoring the stock

        Returns:
            tuple: (bool, str) - (success, error_message)
        """
        if not self.symbol:
            return False, "No stock symbol set"

        # Check if market is currently open
        if not is_market_hours(self.config):
            self.alert_system.display_warning(
                "Market is currently closed. Monitoring will start when market opens."
            )

        # Fetch opening price
        success, error = self.fetch_opening_price()
        if not success:
            return False, f"Failed to fetch opening price: {error}"

        # Set monitoring flag
        self.is_monitoring = True

        # Display monitoring info
        self.alert_system.display_info(
            f"Monitoring {self.symbol} with {self.config.get('threshold_percent', 5.0)}% threshold"
        )
        self.alert_system.display_info(
            f"Checking every {self.check_interval} minutes during market hours (09:15 - 15:30 IST)"
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
        """Stop monitoring the stock"""
        self.is_monitoring = False
        schedule.clear()

        # Display final info if market is closed
        if self.symbol and self.opening_price:
            current_price, error = self.api_client.get_current_price(self.symbol)
            if not error and current_price:
                percentage_change = calculate_percentage_change(current_price, self.opening_price)
                timestamp = get_timestamp()
                self.alert_system.display_closing_info(
                    self.symbol,
                    current_price,
                    self.opening_price,
                    percentage_change,
                    timestamp
                )

        self.alert_system.display_info("\nMonitoring stopped.")

    def get_current_status(self):
        """
        Get current monitoring status

        Returns:
            dict: Status information
        """
        if not self.is_monitoring:
            return {'monitoring': False}

        current_price, error = self.api_client.get_current_price(self.symbol)
        if error:
            return {
                'monitoring': True,
                'symbol': self.symbol,
                'error': error
            }

        percentage_change = calculate_percentage_change(current_price, self.opening_price)

        return {
            'monitoring': True,
            'symbol': self.symbol,
            'opening_price': self.opening_price,
            'current_price': current_price,
            'percentage_change': percentage_change,
            'in_market_hours': is_market_hours(self.config)
        }
