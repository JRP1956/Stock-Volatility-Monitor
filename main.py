#!/usr/bin/env python3
"""
Stock Volatility Monitor - Main Entry Point
Phase 1: MVP
"""
import sys
from colorama import Fore, Style, init
from src.stock_monitor import StockMonitor
from src.utils import load_config, validate_stock_symbol

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Display application banner"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}")
    print("     STOCK VOLATILITY MONITOR - PHASE 1 MVP")
    print(f"{'='*60}{Style.RESET_ALL}\n")


def get_stock_input():
    """
    Get stock symbol from user

    Returns:
        str: Stock symbol or None if user wants to quit
    """
    print(f"{Fore.YELLOW}Enter stock symbol in NSE/BSE format{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Examples: RELIANCE.NS, TCS.NS, INFY.BO{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}(or 'q' to quit){Style.RESET_ALL}\n")

    symbol = input("Stock Symbol: ").strip().upper()

    if symbol.lower() == 'q':
        return None

    return symbol


def main():
    """Main application entry point"""
    try:
        # Display banner
        print_banner()

        # Load configuration
        config = load_config()
        if not config:
            print(f"{Fore.RED}Failed to load configuration. Exiting.{Style.RESET_ALL}")
            sys.exit(1)

        # Display configuration info
        threshold = config.get('threshold_percent', 5.0)
        interval = config.get('check_interval_minutes', 5)
        print(f"{Fore.CYAN}Configuration:{Style.RESET_ALL}")
        print(f"  - Volatility Threshold: {threshold}%")
        print(f"  - Check Interval: {interval} minutes")
        print(f"  - Market Hours: {config.get('market_open_time')} - {config.get('market_close_time')} IST\n")

        # Get stock symbol from user
        while True:
            symbol = get_stock_input()

            if symbol is None:
                print(f"\n{Fore.CYAN}Exiting. Goodbye!{Style.RESET_ALL}")
                sys.exit(0)

            # Validate symbol format
            if not validate_stock_symbol(symbol):
                print(f"{Fore.RED}Invalid format! Symbol must end with .NS (NSE) or .BO (BSE){Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Examples: RELIANCE.NS, TCS.NS, INFY.BO{Style.RESET_ALL}\n")
                continue

            # Create monitor instance
            monitor = StockMonitor(config)

            # Set stock symbol
            success, error = monitor.set_stock(symbol)
            if not success:
                print(f"{Fore.RED}{error}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please try another symbol.{Style.RESET_ALL}\n")
                continue

            # Start monitoring
            print(f"\n{Fore.GREEN}✓ Stock symbol validated: {symbol}{Style.RESET_ALL}\n")
            success, error = monitor.start_monitoring()

            if not success:
                print(f"{Fore.RED}Failed to start monitoring: {error}{Style.RESET_ALL}\n")
                continue

            # Ask if user wants to monitor another stock
            print(f"\n{Fore.YELLOW}Monitor another stock? (y/n): {Style.RESET_ALL}", end="")
            choice = input().strip().lower()
            if choice != 'y':
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}Monitoring interrupted by user. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
