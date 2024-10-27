from src.services.stock.basic.stock_history import get_history_metadata
import numpy as np
import pandas as pd

def five_year_cagr(symbol, period):
    tes = get_history_metadata(symbol, period)
    # tes2 = tes['Close'].iloc[:-1]
    first = tes['Close'].iloc[0]
    last = tes['Close'].iloc[-1]
    periods = 5
    cagr = (last/first)**(1/periods)-1
    # print("first: ",first)
    # print("last: ",last)
    # print("tes2: ",tes2)
    print(f"cagr, {cagr:.4%}")
    return cagr


def five_year_max_drawdown(symbol, period):
    tes = get_history_metadata(symbol, period)
    # tes2 = tes['Close'].iloc[:-1]
    rolling_max = tes['Close'].cummax()

    drawdown = (tes['Close'] - rolling_max) / rolling_max

    max_drawdown = drawdown.min()
    # Find the trough value (minimum during drawdown period)
    trough_value = tes['Close'][drawdown.idxmin()]

    trough_value2 = tes['Close'].min()
    
   
    # print("first: ",first)
    # print("last: ",last)
    print(f"max drawdown: {max_drawdown:.2%}") #
    # print("drawdown: ",drawdown)
    # print("trough_value: ",trough_value)
    # print(f"trough_value2: {trough_value2}",)
    return max_drawdown

    # print("max_drawdown_percent",max_drawdown_percent)
    # return max_drawdown_percent


def calculate_volatility(symbol, period):
    tes = get_history_metadata(symbol, period)

    tes['Log_Ret'] = np.log(tes['Close'] / tes['Close'].shift(1))
    tes['Volatility'] = tes['Log_Ret'].rolling(window=252).std() * np.sqrt(252)
    # print(tes)

    # Calculate daily returns
    daily_returns = tes['Close'].pct_change().dropna()

    # Calculate annualized volatility (standard deviation)
    volatility = daily_returns.std() * np.sqrt(252)  # Assuming 252 trading days per year

    print(f"Annualized Volatility: {volatility:.2%}")
    return volatility


def beta_to_ihsg(symbol, period):
    market_data = get_history_metadata('%5EJKSE', '5y')
    # print(f'market data: {market_data}')
    market_returns = market_data['Close'].pct_change().dropna()
    
    stock_data = get_history_metadata(symbol, period)
    stock_returns = stock_data['Close'].pct_change().dropna()

    returns_data = pd.DataFrame({
    'Stock Returns': stock_returns,
    'Market Returns': market_returns,}).dropna()

    # print('returns data: ',returns_data)

    cov_matrix = returns_data.cov()
    cov_stock_to_market = cov_matrix.iloc[0, 1]  

    var_market = returns_data['Market Returns'].var()

    beta = cov_stock_to_market / var_market

    print(f'beta1: {beta}')
    return beta


def alpha_to_ihsg(symbol, period):
    market_data = get_history_metadata('%5EJKSE', '5y')
    market_return = (market_data['Close'].iloc[-1] - market_data['Close'].iloc[0]) / market_data['Close'].iloc[0]

    stock_data = get_history_metadata(symbol, period)
    stock_return = (stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]

    risk_free_rate = 0.065
    beta = beta_to_ihsg(symbol, period)

    alpha = stock_return - (risk_free_rate + beta * (market_return - risk_free_rate))

    print(f"Alpha: {alpha}")
    return alpha





