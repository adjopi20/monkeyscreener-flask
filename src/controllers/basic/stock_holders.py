from flask import Blueprint, jsonify
import yfinance as yf 
from src.utils.add_jk import addJK
import logging

holders_bp = Blueprint('holders', __name__)

symbol_arr = addJK()

@holders_bp.route('/api/holders/<symbol>', methods=['GET'])
def get_holders(symbol):
    try:
        stock = yf.Ticker(symbol)
        major_holders = stock.major_holders
        institutional_holders = stock.institutional_holders 
        mutualfund_holders = stock.mutualfund_holders
        insider_transaction = stock.insider_transactions
        insider_purchases = stock.insider_purchases
        insider_roster_holders = stock.insider_roster_holders


        return jsonify({
            'major_holders': major_holders.to_dict,
            'institutional_holders': institutional_holders.to_dict(),
            'mutualfund_holders': mutualfund_holders.to_dict(),
            'insider_transactions': insider_transaction.to_dict(),
            'insider_purchases': insider_purchases.to_dict(),
            'insider_roster_holders': insider_roster_holders.to_dict(),
            'symbol': symbol
        })
    except Exception as e:
        logging.error(f"Error getting stock info for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500  
    
@holders_bp.route('/api/major-holders/<symbol>', methods=['GET'])
def get_major_holders(symbol):
    
    try:
        stock = yf.Ticker(symbol)
        tes = stock.major_holders
        print(f'major_holders: {tes}')
        if tes is not None and not tes.empty:
            # Convert to dict and return JSON
            return jsonify({
                'symbol': symbol,
                'major_holders': tes.to_dict(orient='index')
            })
        else:
            # Handle cases where no major holders are found
            return jsonify({
                'symbol': symbol,
                'major_holders': None,
                'message': 'No major holders data found.'
            }), 404

    except Exception as e:
        logging.error(f"Error getting major holders for {symbol}: {e}")
        return jsonify({
            'error': str(e),
            'message': f"Failed to retrieve major holders for {symbol}"
        }), 500
    
@holders_bp.route('/api/major-holders', methods=['GET'])
def get_all_major_holders():
    holders_arr = []
    for symbol in symbol_arr:
        try:
            stock = yf.Ticker(symbol)
            major_holders = stock.major_holders
            holders_arr.append({
                'symbol': symbol,
                'major_holders': major_holders.to_dict(orient='index')
            })
        except Exception as e:
            logging.error(f"error getting symbol for {symbol}: {e}")
    return jsonify(holders_arr)
