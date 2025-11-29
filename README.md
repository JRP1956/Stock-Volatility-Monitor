# Stock Volatility Monitor - Phase 1 MVP

A Python-based terminal application that monitors Indian stock market prices and sends alerts when a stock's price movement exceeds a specified threshold (5% by default).

## Features (Phase 1)

- Monitor single stock from NSE/BSE
- Real-time price tracking during market hours
- Terminal-based colored alerts
- Alert history logging
- Configurable volatility threshold
- Market hours detection (9:15 AM - 3:30 PM IST)

## Prerequisites

- Python 3.8 or higher
- Internet connection for API access

## Installation

1. Clone or navigate to the project directory:
```bash
cd Stock-Volatility
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to customize settings:

```yaml
threshold_percent: 5.0              # Alert when price changes by this %
check_interval_minutes: 5           # How often to check prices
market_open_time: "09:15"          # NSE opening time (IST)
market_close_time: "15:30"         # NSE closing time (IST)
alert_cooldown_minutes: 30         # Minimum time between alerts
```

## Usage

### Starting the Monitor

```bash
python main.py
```

### Entering Stock Symbols

When prompted, enter stock symbols in the following format:

**NSE Stocks:** Add `.NS` suffix
```
RELIANCE.NS
TCS.NS
INFY.NS
HDFCBANK.NS
```

**BSE Stocks:** Add `.BO` suffix
```
RELIANCE.BO
TCS.BO
```

### Example Session

```
============================================================
     STOCK VOLATILITY MONITOR - PHASE 1 MVP
============================================================

Configuration:
  - Volatility Threshold: 5.0%
  - Check Interval: 5 minutes
  - Market Hours: 09:15 - 15:30 IST

Enter stock symbol in NSE/BSE format
Examples: RELIANCE.NS, TCS.NS, INFY.BO
(or 'q' to quit)

Stock Symbol: TCS.NS

✓ Stock symbol validated: TCS.NS

[09:15:00] ✓ TCS.NS - Market Open: ₹3,450.00
ℹ Monitoring TCS.NS with 5.0% threshold
ℹ Checking every 5 minutes during market hours (09:15 - 15:30 IST)
ℹ Press Ctrl+C to stop monitoring

[09:20:00] TCS.NS - Current: ₹3,455.00 (+0.14%)
[09:25:00] TCS.NS - Current: ₹3,478.00 (+0.81%)
...
[11:45:00]
============================================================
🚨 VOLATILITY ALERT! 🚨
Symbol: TCS.NS
Opening Price: ₹3,450.00
Current Price: ₹3,623.00
Change: ↑ +5.01% (UP)
============================================================

[15:30:00] Market Closed - TCS.NS
Final Price: ₹3,610.00 (+4.64%)
```

### Stopping the Monitor

Press `Ctrl+C` to stop monitoring at any time.

## Project Structure

```
Stock-Volatility/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── src/
│   ├── __init__.py
│   ├── stock_monitor.py        # Core monitoring logic
│   ├── api_client.py           # Yahoo Finance API client
│   ├── alert_system.py         # Alert handling and display
│   └── utils.py                # Helper functions
│
├── data/
│   └── alerts_history.json     # Alert logs (auto-generated)
│
└── config/
    └── config.yaml             # Configuration settings
```

## Alert History

All alerts are automatically logged to `data/alerts_history.json` with the following information:

```json
[
  {
    "timestamp": "2025-11-29 11:45:30",
    "symbol": "TCS.NS",
    "opening_price": 3450.0,
    "current_price": 3623.0,
    "percentage_change": 5.01,
    "direction": "UP"
  }
]
```

## How It Works

1. **Initialization:** Application loads configuration and validates user input
2. **Opening Price:** Fetches the stock's opening price at market open
3. **Periodic Checks:** Every N minutes (default: 5), fetches current price
4. **Calculation:** Computes percentage change from opening price
5. **Alert Trigger:** If |change| > threshold, displays colored alert
6. **Logging:** Saves alert details to JSON file

## Market Hours

The monitor only checks prices during NSE trading hours:
- Monday to Friday
- 9:15 AM to 3:30 PM IST
- Outside these hours, monitoring pauses automatically

## Color Coding

- **Green:** Positive price movement (stock going up)
- **Red:** Negative price movement (stock going down)
- **Yellow:** Warnings and info messages
- **Cyan:** General information

## Error Handling

The application handles:
- Invalid stock symbols
- API timeouts (retries up to 3 times)
- Network failures (continues monitoring)
- Market closed scenarios

## Troubleshooting

### "Invalid stock symbol" error
- Ensure you're using the correct format: `SYMBOL.NS` or `SYMBOL.BO`
- Verify the stock exists on NSE/BSE
- Check your internet connection

### "No data available" error
- The stock might not have traded today
- Market might be closed
- Try a different stock symbol

### API timeouts
- Check your internet connection
- The Yahoo Finance API might be temporarily unavailable
- The application will retry automatically

## Future Enhancements (Planned)

- Phase 2: Multiple stock monitoring, desktop notifications
- Phase 3: Email/SMS alerts, web dashboard, ML predictions

## Dependencies

- `yfinance` - Stock data from Yahoo Finance
- `pandas` - Data manipulation
- `schedule` - Job scheduling
- `colorama` - Colored terminal output
- `python-dateutil` - Date/time utilities
- `pytz` - Timezone handling
- `pyyaml` - Configuration file parsing

## License

This is an educational project for learning Python and stock market APIs.

## Support

For issues or questions, refer to the project documentation or check the Yahoo Finance API status.
