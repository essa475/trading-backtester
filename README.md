# TradeBacktester
## Install
Install Python 3.10+, then:
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## CSV
Required: Date, Open, High, Low, Close. Volume optional.

## Strategy
The default Midpoint Retracement Strategy calculates `(previous_high + previous_low) / 2` and enters BUY when the current candle range touches that level. Stop loss defaults to previous candle low and take profit uses configurable risk/reward.

## Important
This educational backtester is a simplified OHLC simulation. Intrabar sequencing, spreads, commissions, slippage, ATR stops, SELL logic, advanced templates and PDF reporting should be extended before relying on it for live trading decisions.
