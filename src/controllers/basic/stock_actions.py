from flask import Blueprint, jsonify
import yfinance as yf 
from src.utils.add_jk import addJK
from src.utils.convertTimestamp import convert_timestamp
import logging

actions_bp = Blueprint('actions', __name__)

@actions_bp.route('/api/actions/<symbol>', methods=['GET'])
def get_actions(symbol):
    try:
        stock = yf.Ticker(symbol)   
        actions = stock.actions
        actions_dict = convert_timestamp(actions.to_dict())
        if actions_dict is not None :
            return jsonify(actions_dict)
        else:
            return {}
    except Exception as e:
        logging.error(f"Error getting stock info for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500
    
@actions_bp.route('/api/actions', methods=['GET'])
def get_all_actions():
    actions_arr = []
    symbol_arr = addJK()
    for symbol in symbol_arr:
        try:
            stock = yf.Ticker(symbol)
            actions = stock.actions
            actions_dict = convert_timestamp(actions.to_dict())
            actions_arr.append({
                'symbol': symbol,
                'actions': actions_dict
            })
        except Exception as e:
            logging.error(f"error getting symbol for {symbol}: {e}")
    return jsonify(actions_arr)

