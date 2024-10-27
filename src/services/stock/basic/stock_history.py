from flask import  jsonify, request
import yfinance as yf
from src.utils.convertTimestamp import convert_timestamp
import logging
import pandas as pd

def get_history_metadata(symbol, period):
    try:

        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)

        hist_dict = convert_timestamp(hist.to_dict()) 
        # metadata = stock.history_metadata
        hist_pd= pd.DataFrame(hist_dict)

        # print(hist_pd)
        return hist_pd

    except Exception as e:
        logging.error(f"Error getting stock info for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500

# get_history_metadata('ASII.JK', '5y')