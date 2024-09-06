
from flask import jsonify, request
import json
import pydantic
import yfinance as yf 
import pandas as pd
from src.utils.add_jk import addJK
from src.utils.convertTimestamp import convert_timestamp
from src.services.stock_info_service import scrape_stock_with_cache
import logging
from src.configs.cache_config import client, cache_ttl
from typing import List, Dict



def get_all_history_metadata2(period):
    stock_arr = []
    scraped_stock = scrape_stock_with_cache()

    for item in scraped_stock:
        symbol = item['symbol']
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            
            if hist.empty:
                continue
            else:
                hist_dict = convert_timestamp(hist.to_dict())
                metadata = stock.history_metadata

                stock_arr.append({
                    'history': hist_dict,
                    'metadata': metadata
                })
        except Exception as e:
            logging.error(f"error getting symbol for {symbol}: {e}")
    print(f"stock_history.get_all_history_metadata: {len(stock_arr)}")
    return {'data': stock_arr, 'count': len(stock_arr)}

    
def calculate_percent_change(start_price: float, end_price: float) -> float:
    return ((end_price - start_price) / start_price) * 100

def process_historical_data(historical_data: List[Dict]) -> Dict:
    daily_gainers = []
    weekly_gainers = []
    monthly_gainers = []
    daily_losers = []
    weekly_losers = []
    monthly_losers = []
    top_volumes = []

    # Process top gainers and losers
    for item in historical_data:
        close = item['history']['Close']
        volumes = item['history']['Volume']
        dates = sorted(close.keys())
        latest = dates[-1]
        latest_price = close[latest]
        end = dates[-2]
        end_price = close[end]
        start = dates[-3]
        start_price = close[start]
        volume = volumes[end]
        symbol = item['metadata']['symbol']

        percent_change = calculate_percent_change(start_price, end_price)

        tes = {
            'symbol': symbol,
            'price': latest_price,
            'percentChange': round(percent_change, 2),
            'lastDayVolume': volume,
        }
        daily_gainers.append(tes)
        daily_losers.append(tes)
        top_volumes.append(tes)

    sorted_percent_change = sorted(daily_gainers, key=lambda x: x['percentChange'], reverse=True)
    daily_gainers = sorted_percent_change[:10]
    daily_losers = sorted_percent_change[-10:]

    sorted_volume = sorted(top_volumes, key=lambda x: x['lastDayVolume'], reverse=True)
    top_volumes = sorted_volume[:12]

    # Weekly Gainers
    for item in historical_data:
        close = item['history']['Close']
        dates = sorted(close.keys())
        latest = dates[-1]
        latest_price = close[latest]
        start = dates[-7]
        start_price = close[start]
        end = dates[-2]
        end_price = close[end]

        percent_change = calculate_percent_change(start_price, end_price)

        tes = {
            'symbol': item['metadata']['symbol'],
            'price': latest_price,
            'percentChange': round(percent_change, 2),
        }
        weekly_gainers.append(tes)

    sorted_weekly_percent_change = sorted(weekly_gainers, key=lambda x: x['percentChange'], reverse=True)
    weekly_gainers = sorted_weekly_percent_change[:10]
    weekly_losers = sorted_weekly_percent_change[-10:]

    # Monthly Gainers
    for item in historical_data:
        close = item['history']['Close']
        dates = sorted(close.keys())
        latest = dates[-1]
        latest_price = close[latest]
        start = dates[1]
        start_price = close[start]
        end = dates[-2]
        end_price = close[end]

        percent_change = calculate_percent_change(start_price, end_price)

        tes = {
            'symbol': item['metadata']['symbol'],
            'price': latest_price,
            'percentChange': round(percent_change, 2),
        }
        monthly_gainers.append(tes)

    sorted_monthly_percent_change = sorted(monthly_gainers, key=lambda x: x['percentChange'], reverse=True)
    monthly_gainers = sorted_monthly_percent_change[:10]
    monthly_losers = sorted_monthly_percent_change[-10:]

    return {
        'dailyGainers': daily_gainers,
        'dailyLosers': daily_losers,
        'weeklyGainers': weekly_gainers,
        'weeklyLosers': weekly_losers,
        'monthlyGainers': monthly_gainers,
        'monthlyLosers': monthly_losers,
        'topVolumes': top_volumes,
    }