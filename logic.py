import yfinance as yf
import pandas as pd
import numpy as np
import json

from sklearn.ensemble import RandomForestClassifier

tickers = [
    "AAPL", "MSFT", "NVDA",
    "AMZN", "META", "GOOGL",
    "JPM", "XOM", "LLY", "COST"
]

benchmark = "SPY"

start_date = "2018-01-01"
end_date = "2025-01-01"

data = yf.download(
    tickers + [benchmark],
    start=start_date,
    end=end_date,
    auto_adjust=True
)

def create_features(data, ticker):
    df = pd.DataFrame()

    df["close"] = data["Close"][ticker]
    df["volume"] = data["Volume"][ticker]

    df["daily_return"] = df["close"].pct_change()

    df["return_5d"] = df["close"].pct_change(5)
    df["return_20d"] = df["close"].pct_change(20)

    df["volatility_20d"] = (
        df["daily_return"]
        .rolling(20)
        .std()
    )

    df["moving_avg_20d"] = (
        df["close"]
        .rolling(20)
        .mean()
    )

    df["moving_avg_ratio"] = (
        df["close"] / df["moving_avg_20d"]
    )

    df["volume_ratio"] = (
        df["volume"] /
        df["volume"].rolling(20).mean()
    )

    df["ticker"] = ticker

    return df

spy_close = data["Close"][benchmark]
spy_future_returns = spy_close.pct_change(5)

all_data = []

for ticker in tickers:

    stock_df = create_features(data, ticker)

    stock_df["future_return_5d"] = (
        stock_df["close"]
        .pct_change(5)
        .shift(-5)
    )

    stock_df["spy_future_return_5d"] = (
        spy_future_returns.shift(-5)
    )

    stock_df["target"] = (
        stock_df["future_return_5d"]
        > stock_df["spy_future_return_5d"]
    ).astype(int)

    all_data.append(stock_df)

dataset = pd.concat(all_data)
dataset = dataset.dropna()

features = [
    "return_5d",
    "return_20d",
    "volatility_20d",
    "moving_avg_ratio",
    "volume_ratio"
]

split_date = "2023-01-01"

train = dataset[dataset.index < split_date]
test = dataset[dataset.index >= split_date]

X_train = train[features]
y_train = train["target"]

X_test = test[features]

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

test = test.copy()

test["predicted_score"] = (
    model.predict_proba(X_test)[:, 1]
)

portfolio_returns = []

for date, group in test.groupby(test.index):

    top_stocks = (
        group
        .sort_values(
            "predicted_score",
            ascending=False
        )
        .head(3)
    )

    strategy_return = (
        top_stocks["future_return_5d"]
        .mean()
    )

    portfolio_returns.append({
        "date": str(date.date()),
        "strategy_return": float(strategy_return)
    })

performance = pd.DataFrame(portfolio_returns)

performance["strategy_cumulative"] = (
    1 + performance["strategy_return"]
).cumprod()

# SPY BENCHMARK
spy_test = (
    spy_future_returns
    .loc[performance["date"]]
    .values
)

performance["spy_return"] = spy_test

performance["spy_cumulative"] = (
    1 + performance["spy_return"]
).cumprod()

performance_json = performance.to_dict(
    orient="records"
)

with open(
    "data/performance.json",
    "w"
) as f:
    json.dump(performance_json, f)

# FEATURE IMPORTANCE

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance_json = (
    importance.to_dict(orient="records")
)

with open(
    "data/feature_importance.json",
    "w"
) as f:
    json.dump(importance_json, f)

# LATEST PICKS

latest_date = test.index.max()

latest_picks = (
    test[test.index == latest_date]
    .sort_values(
        "predicted_score",
        ascending=False
    )
    .head(5)
)

latest_json = latest_picks[
    [
        "ticker",
        "predicted_score",
        "return_5d",
        "return_20d",
        "volatility_20d"
    ]
].to_dict(orient="records")

with open(
    "data/latest_picks.json",
    "w"
) as f:
    json.dump(latest_json, f)

print("Data exported successfully")
