from src.services.stock.basic.stock_history import get_history_metadata
import numpy as np

def five_year_cagr_close():
    tes = get_history_metadata('ASII.JK', '5y')
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

five_year_cagr_close()

def five_year_max_drawdown_close():
    tes = get_history_metadata('ASII.JK', '5y')
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

five_year_max_drawdown_close()

def volatility():
    tes = get_history_metadata('ASII.JK', '5y')
    # Calculate daily returns
    daily_returns = tes['Close'].pct_change().dropna()

    # Calculate annualized volatility (standard deviation)
    volatility = daily_returns.std() * np.sqrt(1260)  # Assuming 252 trading days per year

    print(f"Annualized Volatility: {volatility:.2%}")



