from flask import Blueprint, jsonify
import yfinance as yf
from src.utils.add_jk import addJK
from src.utils.convertTimestamp import convert_timestamp
import logging

recommendations_bp = Blueprint('recommendations', __name__)

symbol_arr = addJK()

@recommendations_bp.route('/api/recommendations/<symbol>', methods=['GET'])
def get_recommendations(symbol):
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations
        recommendations_dict = convert_timestamp(recommendations.to_dict())
        upgrades_downgrades = stock.upgrades_downgrades
        upgrades_downgrades_dict = convert_timestamp(upgrades_downgrades.to_dict())
        return jsonify({
            'recommendations': recommendations_dict,
            'upgrades_downgrades': upgrades_downgrades_dict,
            'symbol': symbol
        })
    except Exception as e:
        logging.error(f"Error getting stock info for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500  
    
@recommendations_bp.route('/api/recommendations', methods=['GET'])
def get_all_recommendations():
    recommendations_arr = []
    for symbol in symbol_arr:
        try:
            stock = yf.Ticker(symbol)
            recommendations = stock.recommendations
            recommendations_dict = convert_timestamp(recommendations.to_dict())
            upgrades_downgrades = stock.upgrades_downgrades
            upgrades_downgrades_dict = convert_timestamp(upgrades_downgrades.to_dict())
            recommendations_arr.append({
                'symbol': symbol,
                'recommendations': recommendations_dict,
                'upgrades_downgrades': upgrades_downgrades_dict
            })
        except Exception as e:
            logging.error(f"error getting symbol for {symbol}: {e}")
    return jsonify(recommendations_arr)

