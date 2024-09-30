from flask import Blueprint, jsonify, request
import json
import yfinance as yf 
from src.utils.convertTimestamp import convert_timestamp
from src.services.stock.basic.stock_info_service import scrape_stock_with_cache
from src.services.stock.calculation.top_gainer import process_historical_data, get_all_history_metadata2
import logging
from src.configs.cache_config import client, cache_ttl

history_bp = Blueprint('history', __name__)

# symbol_arr = addJK

@history_bp.route('/api/history-metadata/<period>', methods=['GET'])
def get_all_history_metadata(period ):
    cache_key = f'all_historical_price_{period}'
    stock_arr = []
    scraped_stock = scrape_stock_with_cache()
    
    cached_raw_value = client.get(cache_key)
    
    if cached_raw_value is not None:
        # Use the TypeAdapter or json.loads if you need to deserialize JSON
        retrieved_data = json.loads(cached_raw_value)
        print(f"stock_history.get_all_history_metadata: {len(retrieved_data)}")
        return jsonify({'data':retrieved_data,
                 'count': len(retrieved_data)})
    
    else: 
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
        
            # Cache the result
        raw_value = json.dumps([stock for stock in stock_arr])
        client.set(cache_key, raw_value, ex=cache_ttl)
        
        return jsonify({'data':stock_arr,
                        'count': len(stock_arr)})

    
   

@history_bp.route('/api/history-metadata/<symbol>/<period>', methods=['GET'])
def get_history_metadata(symbol, period):
    try:
        start = request.args.get('start')
        end = request.args.get('end')

        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, start=start, end=end)

        hist_dict = convert_timestamp(hist.to_dict()) 
        metadata = stock.history_metadata

        return jsonify({
            'history': hist_dict,
            'metadata': metadata
        })

    except Exception as e:
        logging.error(f"Error getting stock info for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500
    
@history_bp.route('/api/top-gainer/<period>', methods=['GET'])
def top_gainer(period):
    cache_key = f'top_gainer_{period}'
    cached_raw_value = client.get(cache_key)

    if cached_raw_value is not None:
        # Use the TypeAdapter or json.loads if you need to deserialize JSON
        retrieved_data = json.loads(cached_raw_value)
        return jsonify(retrieved_data)
    else:
        historical_data = get_all_history_metadata2(period)['data']
        processed_data = process_historical_data(historical_data)
        raw_value = json.dumps(processed_data)
        client.set(cache_key, raw_value, ex=cache_ttl)
        return jsonify(processed_data)
    
