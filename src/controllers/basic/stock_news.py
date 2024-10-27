from flask import Blueprint, jsonify
import yfinance as yf
from src.utils.add_jk import addJK
import logging
from src.configs.cache_config import client, cache_ttl
import json

news_bp = Blueprint('news', __name__)

symbol_arr = addJK()

@news_bp.route('/api/news/<symbol>', methods=['GET'])
def get_test(symbol):
    stock = yf.Ticker(symbol)
    news = stock.news
    return jsonify(news)

@news_bp.route('/api/news', methods=['GET'])
def get_all_news():
    cached_key = "all-news"
    
    
    
    
    try:

        cached_raw_value = client.get(cached_key)

        if cached_raw_value is not None:
        
            cached_news = json.loads(cached_raw_value)
            return jsonify(cached_news)
        
        stock = yf.Ticker('AALI.JK')
        news = stock.news
        
        cached=json.dumps(news)
        client.set(cached_key, cached, ex=cache_ttl)
        return jsonify(news)
    
    except Exception as e:
        logging.error(f"found error: {e}")
        print(f"found error: {e}")