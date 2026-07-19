import yfinance as yf
import pandas as pd
import numpy as np

# Inputs
ticker = "BTC-USD"
years = 10
initial_capital = 10000

# Download data
df = yf.download(ticker, period=f"{years}y")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Strategy
df["SMA50"] = df["Close"].rolling(50).mean()
df["SMA200"] = df["Close"].rolling(200).mean()

df["Signal"] = np.where(df["SMA50"] > df["SMA200"], "BUY", "SELL")

df["Prev_Signal"] = df["Signal"].shift(1)
df["Trade"] = np.where(df["Signal"] != df["Prev_Signal"], df["Signal"], "")

df["Trade_Price"] = df["Close"].shift(-1).where(df["Trade"] != "")

df_full = df.copy()

# Remove rows without trades and remove first "SELL"
df = df[df["Trade"] != ""]
if not df.empty and df.iloc[0]["Trade"] == "SELL":
    df = df.iloc[1:]

# Build trades dataframe
trades = []

entry_price = None
entry_date = None

for i in range(len(df)):
    trade = df["Trade"].iloc[i]
    price = df["Trade_Price"].iloc[i]
    date = df.index[i]

    if trade == "BUY":
        entry_price = price
        entry_date = date

    elif trade == "SELL" and entry_price is not None:
        exit_price = price
        exit_date = date

        ret = (exit_price - entry_price) / entry_price

        trades.append({
            "Entry Date": entry_date,
            "Exit Date": exit_date,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Return": ret
        })

        entry_price = None
        entry_date = None

# If the last position is still open (BUY without SELL), close it today
if entry_price is not None:
    # Take the last price available from the original dataset
    exit_price = df["Close"].iloc[-1]
    exit_date = df.index[-1]
    ret = (exit_price - entry_price) / entry_price
    trades.append({
        "Entry Date": entry_date,
        "Exit Date": exit_date,
        "Entry Price": entry_price,
        "Exit Price": exit_price,
        "Return": ret
    })

trades_df = pd.DataFrame(trades)

# Equity
trades_df["Equity"] = initial_capital * (1 + trades_df["Return"]).cumprod()

# Drawdown
trades_df["Peak"] = trades_df["Equity"].cummax()
trades_df["Drawdown"] = (trades_df["Equity"] - trades_df["Peak"]) / trades_df["Peak"]

# Max drawdown
max_drawdown = trades_df["Drawdown"].min()
# Win rate
win_rate = (trades_df["Return"] > 0).mean()
# Sharpe ratio
strategy_returns = trades_df["Return"]
strategy_sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(len(strategy_returns))

# Compare with buy&hold
    # Daily return
df["Return"] = df["Close"].pct_change()
    # Equity
df["BH_Equity"] = initial_capital * (1 + df["Return"]).cumprod()
    # Sharpe ratio
bh_returns = df["Return"].dropna()
bh_sharpe = bh_returns.mean() / bh_returns.std() * np.sqrt(252)

# Metrics
print("Max Drawdown:", round(max_drawdown * 100, 2), "%")
print("Win Rate:", round(win_rate * 100, 2), "%")
print("Strategy Sharpe:", round(strategy_sharpe, 2))
print("Buy & Hold Sharpe:", round(bh_sharpe, 2))

# Export
trades_df.to_excel('/Users/Carlo/Desktop/Trades.xlsx', index=False)

# Equity curves chart
plt.figure()
    # Straetgy Equity
plt.plot(trades_df["Exit Date"], trades_df["Equity"], label="Strategy")
    # B&h Equity
plt.plot(df.index, df["BH_Equity"], label="Buy & Hold")
plt.legend()
plt.title("Equity Curve Comparison")
plt.show()
