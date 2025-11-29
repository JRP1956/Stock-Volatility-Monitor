# Stock Volatility Monitor - Phase 2

A Python-based terminal application that monitors multiple Indian stock market prices simultaneously and sends alerts when stock price movements exceed configured thresholds.

## Features

### Phase 2 (Current)
- **Multiple Stock Monitoring** - Monitor up to 10 stocks simultaneously
- **Custom Thresholds** - Set different alert thresholds for each stock
- **Interactive Menu** - Add/remove stocks, view status, start monitoring
- **Per-Stock Configuration** - Customize thresholds for volatile vs stable stocks

### Phase 1 Features
- Real-time price tracking during market hours
- Terminal-based colored alerts
- Alert history logging (JSON)
- Market hours detection (9:15 AM - 3:30 PM IST)
- Configurable check intervals
- Alert cooldown to prevent spam

## Prerequisites

- Python 3.8 or higher
- Internet connection for API access

## Installation

1. **Clone or download the repository:**
```bash
cd Stock-Volatility
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Quick Start

```bash
python main.py
```

Follow the prompts to add stocks and start monitoring.

## Example Session

```
======================================================================
     STOCK VOLATILITY MONITOR - PHASE 2
     Multiple Stocks | Custom Thresholds
======================================================================

Configuration:
  - Default Threshold: 5.0%
  - Check Interval: 5 minutes
  - Market Hours: 09:15 - 15:30 IST

Add stocks to monitor:
Enter stock symbols one at a time (NSE: SYMBOL.NS, BSE: SYMBOL.BO)
Examples: RELIANCE.NS, TCS.NS, INFY.BO
Press Enter with empty input when done

Stock Symbol 1 (or press Enter to finish): TCS.NS
Custom threshold for TCS.NS? (press Enter for default): 3.0
✓ Added TCS.NS (threshold: 3.0%)

Stock Symbol 2 (or press Enter to finish): RELIANCE.NS
Custom threshold for RELIANCE.NS? (press Enter for default): 7.0
✓ Added RELIANCE.NS (threshold: 7.0%)

Stock Symbol 3 (or press Enter to finish):

======================================================================
Options:
  1. Add more stocks
  2. Remove a stock
  3. View current stocks
  4. Start monitoring
  5. Exit
======================================================================

Select option (1-5): 4

Starting monitoring...

[09:15:00] ✓ TCS.NS - Market Open: ₹3,450.00
[09:15:01] ✓ RELIANCE.NS - Market Open: ₹2,800.00

Monitoring 2 stock(s)
  - TCS.NS (threshold: 3.0%)
  - RELIANCE.NS (threshold: 7.0%)

Checking every 5 minutes during market hours (09:15 - 15:30 IST)
Press Ctrl+C to stop monitoring

[09:20:00] TCS.NS - Current: ₹3,455.00 (+0.14%)
[09:20:00] RELIANCE.NS - Current: ₹2,820.00 (+0.71%)
[09:25:00] TCS.NS - Current: ₹3,550.00 (+2.90%)
[09:25:00] RELIANCE.NS - Current: ₹2,850.00 (+1.79%)
...
[11:45:00]
============================================================
🚨 VOLATILITY ALERT! 🚨
Symbol: TCS.NS
Opening Price: ₹3,450.00
Current Price: ₹3,560.00
Change: ↑ +3.19% (UP)
============================================================
```

## Configuration

### Basic Configuration

Edit `config/config.yaml`:

```yaml
# Default threshold for all stocks
threshold_percent: 5.0

# How often to check prices (minutes)
check_interval_minutes: 5

# Market hours (IST)
market_open_time: "09:15"
market_close_time: "15:30"

# Minimum time between repeat alerts (minutes)
alert_cooldown_minutes: 30
```

### Per-Stock Thresholds

Set different thresholds for different stocks in `config/config.yaml`:

```yaml
stock_thresholds:
  TCS.NS: 3.0       # Alert when TCS moves more than 3%
  RELIANCE.NS: 7.0  # Alert when Reliance moves more than 7%
  INFY.NS: 4.0      # Alert when Infosys moves more than 4%
```

These thresholds are **defaults** in the config file. You can also set custom thresholds when adding stocks interactively during runtime.

## Stock Symbol Format

### NSE (National Stock Exchange)
Add `.NS` suffix:
- `TCS.NS`
- `RELIANCE.NS`
- `INFY.NS`
- `HDFCBANK.NS`
- `ITC.NS`

### BSE (Bombay Stock Exchange)
Add `.BO` suffix:
- `TCS.BO`
- `RELIANCE.BO`
- `INFY.BO`

## Interactive Menu Options

### 1. Add More Stocks
Add additional stocks to your monitoring list. You can specify custom thresholds for each stock.

### 2. Remove a Stock
Remove a stock from your monitoring list.

### 3. View Current Stocks
Display all stocks currently being monitored with their thresholds.

### 4. Start Monitoring
Begin monitoring all added stocks. The application will:
- Fetch opening prices for all stocks
- Check prices at configured intervals
- Send terminal alerts when thresholds are exceeded
- Log all alerts to `data/alerts_history.json`

### 5. Exit
Quit the application.

## Alert Example

```
============================================================
🚨 VOLATILITY ALERT! 🚨
Symbol: TCS.NS
Opening Price: ₹3,450.00
Current Price: ₹3,623.00
Change: ↑ +5.01% (UP)
============================================================
```

## Alert History

All alerts are logged to `data/alerts_history.json`:

```json
[
  {
    "timestamp": "2025-11-30 11:45:30",
    "symbol": "TCS.NS",
    "opening_price": 3450.0,
    "current_price": 3623.0,
    "percentage_change": 5.01,
    "direction": "UP"
  }
]
```

## Project Structure

```
Stock-Volatility/
│
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── README.md                        # This file
│
├── config/
│   └── config.yaml                 # Configuration
│
├── data/
│   └── alerts_history.json         # Alert logs (auto-generated)
│
└── src/
    ├── __init__.py
    ├── stock_monitor.py            # Core monitoring logic
    ├── stock_config.py             # Per-stock settings
    ├── api_client.py               # Yahoo Finance API
    ├── alert_system.py             # Alert handling
    └── utils.py                    # Helper functions
```

## How It Works

1. **Initialization**: Load configuration and display settings
2. **Stock Input**: Add multiple stocks with optional custom thresholds
3. **Opening Prices**: Fetch opening prices for all stocks at market open
4. **Periodic Checks**: Every N minutes (default: 5):
   - Fetch current prices for all stocks
   - Calculate percentage change from opening
   - Check if threshold exceeded for each stock
5. **Alert Trigger**: If threshold exceeded:
   - Display terminal alert with color coding
   - Log to JSON file
   - Apply cooldown period to prevent spam
6. **Market Hours**: Only monitors during NSE hours (9:15 AM - 3:30 PM IST, Mon-Fri)

## Market Hours

The monitor only checks prices during NSE trading hours:
- **Days**: Monday to Friday
- **Hours**: 9:15 AM to 3:30 PM IST
- Outside these hours, monitoring pauses automatically

## Troubleshooting

### Stock symbol invalid
- Ensure format: `SYMBOL.NS` (NSE) or `SYMBOL.BO` (BSE)
- Verify stock exists and trades on that exchange

### No price data
- Stock might not have traded today
- Market might be closed
- Check internet connection

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

## Dependencies

- `yfinance` - Stock data from Yahoo Finance
- `pandas` - Data manipulation
- `schedule` - Job scheduling
- `colorama` - Colored terminal output
- `python-dateutil` - Date/time utilities
- `pytz` - Timezone handling
- `pyyaml` - Configuration file parsing

## Future Enhancements (Phase 3)

Planned features:
- Email/SMS alert notifications
- Desktop notifications (macOS/Windows/Linux)
- Alert history viewer in terminal
- Web dashboard
- Historical volatility analysis
- Machine learning price predictions
- Cryptocurrency support
- Technical indicator alerts (RSI, MACD)

## Contributing

This is an educational project. Feel free to fork and customize!

## License

Educational project for learning Python and stock market APIs.

## Changelog

### Phase 2 (Current)
- Added multiple stock monitoring (up to 10 stocks)
- Added per-stock custom thresholds
- Added interactive menu system
- Added stock management (add/remove)
- Enhanced configuration system with stock-specific settings

### Phase 1
- Single stock monitoring
- Terminal-based alerts
- Alert history logging
- Market hours detection
- Basic error handling
