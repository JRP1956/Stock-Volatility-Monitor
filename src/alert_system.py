"""
Alert system for Stock Volatility Monitor
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from colorama import Fore, Style, init
from .utils import format_currency, get_full_timestamp

# Initialize colorama
init(autoreset=True)


class AlertSystem:
    """Handles alerts and logging"""

    def __init__(self, config):
        """
        Initialize alert system

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.threshold = config.get('threshold_percent', 5.0)
        self.cooldown_minutes = config.get('alert_cooldown_minutes', 30)
        self.alerts_file = Path(__file__).parent.parent / "data" / "alerts_history.json"
        self.last_alert_time = {}

    def should_trigger_alert(self, symbol, percentage_change):
        """
        Check if an alert should be triggered

        Args:
            symbol: Stock symbol
            percentage_change: Percentage change from opening price

        Returns:
            bool: True if alert should be triggered
        """
        # Check if absolute percentage exceeds threshold
        if abs(percentage_change) < self.threshold:
            return False

        # Check cooldown period
        if symbol in self.last_alert_time:
            time_since_last = datetime.now() - self.last_alert_time[symbol]
            if time_since_last < timedelta(minutes=self.cooldown_minutes):
                return False

        return True

    def trigger_alert(self, symbol, current_price, opening_price, percentage_change):
        """
        Trigger and display an alert

        Args:
            symbol: Stock symbol
            current_price: Current stock price
            opening_price: Opening stock price
            percentage_change: Percentage change
        """
        # Update last alert time
        self.last_alert_time[symbol] = datetime.now()

        # Determine color based on direction
        if percentage_change > 0:
            color = Fore.GREEN
            direction = "UP"
            arrow = "↑"
        else:
            color = Fore.RED
            direction = "DOWN"
            arrow = "↓"

        # Display alert
        print(f"\n{'='*60}")
        print(f"{color}{Style.BRIGHT}🚨 VOLATILITY ALERT! 🚨{Style.RESET_ALL}")
        print(f"{color}Symbol: {symbol}{Style.RESET_ALL}")
        print(f"Opening Price: {format_currency(opening_price)}")
        print(f"Current Price: {format_currency(current_price)}")
        print(f"{color}{Style.BRIGHT}Change: {arrow} {percentage_change:+.2f}% ({direction}){Style.RESET_ALL}")
        print(f"{'='*60}\n")

        # Log alert
        self._log_alert(symbol, current_price, opening_price, percentage_change)

    def display_status(self, symbol, current_price, opening_price, percentage_change, timestamp):
        """
        Display current status without alert

        Args:
            symbol: Stock symbol
            current_price: Current stock price
            opening_price: Opening stock price
            percentage_change: Percentage change
            timestamp: Current timestamp
        """
        if percentage_change > 0:
            color = Fore.GREEN
            sign = "+"
        elif percentage_change < 0:
            color = Fore.RED
            sign = ""
        else:
            color = Fore.YELLOW
            sign = ""

        print(f"[{timestamp}] {symbol} - Current: {format_currency(current_price)} "
              f"({color}{sign}{percentage_change:.2f}%{Style.RESET_ALL})")

    def display_opening_info(self, symbol, opening_price, timestamp):
        """
        Display market opening information

        Args:
            symbol: Stock symbol
            opening_price: Opening stock price
            timestamp: Current timestamp
        """
        print(f"[{timestamp}] {Fore.GREEN}✓{Style.RESET_ALL} {symbol} - Market Open: {format_currency(opening_price)}")

    def display_closing_info(self, symbol, final_price, opening_price, percentage_change, timestamp):
        """
        Display market closing information

        Args:
            symbol: Stock symbol
            final_price: Final stock price
            opening_price: Opening stock price
            percentage_change: Final percentage change
            timestamp: Current timestamp
        """
        if percentage_change > 0:
            color = Fore.GREEN
            sign = "+"
        else:
            color = Fore.RED
            sign = ""

        print(f"\n[{timestamp}] {Fore.YELLOW}Market Closed{Style.RESET_ALL} - {symbol}")
        print(f"Final Price: {format_currency(final_price)} "
              f"({color}{sign}{percentage_change:.2f}%{Style.RESET_ALL})")

    def _log_alert(self, symbol, current_price, opening_price, percentage_change):
        """
        Log alert to JSON file

        Args:
            symbol: Stock symbol
            current_price: Current stock price
            opening_price: Opening stock price
            percentage_change: Percentage change
        """
        try:
            # Load existing alerts
            if self.alerts_file.exists():
                with open(self.alerts_file, 'r') as f:
                    alerts = json.load(f)
            else:
                alerts = []

            # Add new alert
            alert_entry = {
                'timestamp': get_full_timestamp(),
                'symbol': symbol,
                'opening_price': opening_price,
                'current_price': current_price,
                'percentage_change': round(percentage_change, 2),
                'direction': 'UP' if percentage_change > 0 else 'DOWN'
            }

            alerts.append(alert_entry)

            # Save alerts
            self.alerts_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)

        except Exception as e:
            print(f"{Fore.RED}Error logging alert: {e}{Style.RESET_ALL}")

    def display_error(self, message):
        """
        Display error message

        Args:
            message: Error message to display
        """
        print(f"{Fore.RED}❌ Error: {message}{Style.RESET_ALL}")

    def display_info(self, message):
        """
        Display info message

        Args:
            message: Info message to display
        """
        print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

    def display_warning(self, message):
        """
        Display warning message

        Args:
            message: Warning message to display
        """
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
