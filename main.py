#!/usr/bin/env python3
"""
Stock Volatility Monitor - Main Entry Point
Phase 2: Multiple Stocks + Notifications
"""
import sys
from colorama import Fore, Style, init
from src.stock_monitor import StockMonitor
from src.utils import load_config, validate_stock_symbol

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Display application banner"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print("     STOCK VOLATILITY MONITOR - PHASE 2")
    print("     Multiple Stocks | Custom Thresholds")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def get_stock_inputs(monitor):
    """
    Get multiple stock symbols from user

    Args:
        monitor: StockMonitor instance

    Returns:
        bool: True if at least one stock was added
    """
    print(f"{Fore.YELLOW}Add stocks to monitor:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Enter stock symbols one at a time (NSE: SYMBOL.NS, BSE: SYMBOL.BO){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Examples: RELIANCE.NS, TCS.NS, INFY.BO{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Enter with empty input when done\n{Style.RESET_ALL}")

    stock_count = 0

    while True:
        symbol = input(f"{Fore.CYAN}Stock Symbol {stock_count + 1} (or press Enter to finish): {Style.RESET_ALL}").strip().upper()

        if not symbol:
            break

        # Validate symbol format
        if not validate_stock_symbol(symbol):
            print(f"{Fore.RED}Invalid format! Symbol must end with .NS (NSE) or .BO (BSE){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Examples: RELIANCE.NS, TCS.NS, INFY.BO{Style.RESET_ALL}\n")
            continue

        # Ask for custom threshold
        print(f"{Fore.YELLOW}Custom threshold for {symbol}? (press Enter for default): {Style.RESET_ALL}", end="")
        threshold_input = input().strip()

        threshold = None
        if threshold_input:
            try:
                threshold = float(threshold_input)
                if threshold <= 0:
                    print(f"{Fore.RED}Invalid threshold! Using default.{Style.RESET_ALL}")
                    threshold = None
            except ValueError:
                print(f"{Fore.RED}Invalid threshold! Using default.{Style.RESET_ALL}")
                threshold = None

        # Add stock to monitor
        success, error = monitor.add_stock(symbol, threshold)
        if not success:
            print(f"{Fore.RED}{error}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please try another symbol.{Style.RESET_ALL}\n")
            continue

        stock_count += 1
        threshold_display = f"{threshold}%" if threshold else "default"
        print(f"{Fore.GREEN}✓ Added {symbol} (threshold: {threshold_display}){Style.RESET_ALL}\n")

    return stock_count > 0


def display_menu():
    """Display interactive menu"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("Options:")
    print("  1. Add more stocks")
    print("  2. Remove a stock")
    print("  3. View current stocks")
    print("  4. Start monitoring")
    print("  5. Exit")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def remove_stock_interactive(monitor):
    """Remove a stock interactively"""
    stocks = monitor.get_monitored_stocks()
    if not stocks:
        print(f"{Fore.YELLOW}No stocks to remove.{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.CYAN}Current stocks:{Style.RESET_ALL}")
    for i, symbol in enumerate(stocks, 1):
        print(f"  {i}. {symbol}")

    choice = input(f"\n{Fore.CYAN}Enter number to remove (or Enter to cancel): {Style.RESET_ALL}").strip()

    if not choice:
        return

    try:
        index = int(choice) - 1
        if 0 <= index < len(stocks):
            symbol = stocks[index]
            if monitor.remove_stock(symbol):
                print(f"{Fore.GREEN}✓ Removed {symbol}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}Failed to remove {symbol}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Invalid selection{Style.RESET_ALL}\n")
    except ValueError:
        print(f"{Fore.RED}Invalid input{Style.RESET_ALL}\n")


def view_stocks(monitor):
    """Display current stocks"""
    stocks = monitor.get_monitored_stocks()
    if not stocks:
        print(f"\n{Fore.YELLOW}No stocks added yet.{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.CYAN}Current stocks ({len(stocks)}):{Style.RESET_ALL}")
    for symbol in stocks:
        threshold = monitor.stock_config.get_threshold(symbol)
        print(f"  - {symbol} (threshold: {threshold}%)")
    print()


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
        print(f"  - Default Threshold: {threshold}%")
        print(f"  - Check Interval: {interval} minutes")
        print(f"  - Market Hours: {config.get('market_open_time')} - {config.get('market_close_time')} IST\n")

        # Create monitor instance
        monitor = StockMonitor(config)

        # Get initial stock inputs
        if not get_stock_inputs(monitor):
            print(f"{Fore.YELLOW}No stocks added. Exiting.{Style.RESET_ALL}")
            sys.exit(0)

        # Interactive menu loop
        while True:
            display_menu()
            choice = input(f"{Fore.CYAN}Select option (1-5): {Style.RESET_ALL}").strip()

            if choice == '1':
                # Add more stocks
                print()
                get_stock_inputs(monitor)

            elif choice == '2':
                # Remove a stock
                remove_stock_interactive(monitor)

            elif choice == '3':
                # View current stocks
                view_stocks(monitor)

            elif choice == '4':
                # Start monitoring
                stocks = monitor.get_monitored_stocks()
                if not stocks:
                    print(f"\n{Fore.RED}No stocks to monitor. Add stocks first.{Style.RESET_ALL}\n")
                    continue

                print(f"\n{Fore.GREEN}Starting monitoring...{Style.RESET_ALL}\n")
                success, error = monitor.start_monitoring()

                if not success:
                    print(f"{Fore.RED}Failed to start monitoring: {error}{Style.RESET_ALL}\n")
                    continue

                # Ask if user wants to continue or exit
                print(f"\n{Fore.YELLOW}Continue with another session? (y/n): {Style.RESET_ALL}", end="")
                continue_choice = input().strip().lower()
                if continue_choice != 'y':
                    print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                    break

            elif choice == '5':
                # Exit
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

            else:
                print(f"\n{Fore.RED}Invalid option. Please select 1-5.{Style.RESET_ALL}\n")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}Interrupted by user. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
