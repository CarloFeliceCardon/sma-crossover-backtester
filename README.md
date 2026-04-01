# SMA 50/200 Crossover Backtester

Systematic backtesting of a Golden Cross / Death Cross strategy across 6 asset classes and 7 historical periods (56 combinations total).

## Strategy
Buy when the 50-day SMA crosses above the 200-day SMA (Golden Cross). Sell when it crosses below (Death Cross). Starting capital: $10,000.

## Assets Tested
| Asset | Ticker |
|---|---|
| S&P 500 | ^GSPC |
| MSCI World | URTH |
| MSCI Emerging Markets | EEM |
| MSCI Europe | EZU |
| iShares Gold Trust | IAU |
| Bitcoin | BTC-USD |

## Periods Tested
Last 50y, last 10y, 2000–2010, 2010–2020, last 7y, 2007–2012, 1995–2005.

## Metrics
Max drawdown, win rate, Sharpe ratio, final equity.

## Key Findings
- The strategy works best on strongly trending assets: S&P 500 and Bitcoin produce consistent Sharpe ratios above 1.
- Emerging markets and European equities show strong period-dependency, with performance collapsing in range-bound decades.
- The strategy structurally underperforms buy & hold on a risk-adjusted basis across most assets and periods.

## Requirements
```
pip install yfinance pandas numpy openpyxl
```

## Usage
Place `Strategy.py` and `Backtesting.xlsx` in the same folder, then run:
```
python3 backtestall.py
```
Output: `AlgBacktesting.xlsx`
