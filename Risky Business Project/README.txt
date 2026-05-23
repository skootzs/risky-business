# Risky Business

Machine Learning-Based Quantitative Equity Forecasting Dashboard

## Overview

Risky Business is an end-to-end quantitative equity research project that uses machine learning and factor modeling to predict short-term stock outperformance relative to SPY.

The project combines:
- financial time-series analysis
- feature engineering
- machine learning classification
- portfolio backtesting
- interactive dashboard visualization

The dashboard visualizes strategy performance, feature importance, and model-generated stock rankings using an interactive web interface.

### Data Collection

Historical market data was downloaded using Yahoo Finance (`yfinance`) for a universe of large-cap U.S. equities and SPY as the benchmark.

## Predictive Factors

The model engineers several quantitative factors from historical price and volume data:

### Momentum Factors
- 5-day return
- 20-day return

### Volatility Factor
- 20-day rolling volatility

### Mean-Reversion Factor
- Price relative to 20-day moving average

### Volume Factor
- Relative volume compared to rolling average volume

## Machine Learning Model

A Random Forest classifier was trained to predict whether a stock would outperform SPY over the next 5 trading days.

Prediction target:

```python
future_stock_return > future_spy_return
```

## Backtesting

The strategy:
1. ranks stocks by predicted probability of outperformance
2. selects the top-ranked equities
3. simulates equal-weight portfolio returns
4. compares cumulative performance against SPY


## Dashboard Features

- Interactive strategy performance visualization
- SPY benchmark comparison
- Feature importance chart
- Dynamic stock ranking table
- Quantitative factor explanations

## Technologies Used

### Python
- pandas
- numpy
- yfinance
- scikit-learn

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

## Future Improvements

- XGBoost and LightGBM models
- Walk-forward validation
- Portfolio optimization
- Monte Carlo simulations
- Sector analysis
- Live market data integration

## Author

Gabriella S Maria
University of Washington — ACMS (Data Science & Statistics)