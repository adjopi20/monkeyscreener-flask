from flask import Blueprint, jsonify
import yfinance as yf
from src.utils.convertTimestamp import convert_timestamp
import logging
from src.services.stock_financial_service import *; get_cash_floww

financials_bp = Blueprint('financials', __name__)

@financials_bp.route('/api/financials/inc-stmt/<symbol>', methods=['GET'])
def get_income_statement(symbol):
    res = getIncStmt(symbol)
    return jsonify(res)

@financials_bp.route('/api/financials/q-inc-stmt/<symbol>', methods=['GET'])
def get_q_income_statement(symbol):
    res = getQIncStmt(symbol)
    return jsonify(res)


#========================================================================================
@financials_bp.route('/api/financials/q-balance-sheet/<symbol>', methods=['GET'])   
def get_quarterly_balance_sheet(symbol):
    res= get_q_bal_sheet(symbol)
    return jsonify(res)

@financials_bp.route('/api/financials/balance-sheet/<symbol>', methods=['GET'])   
def get_balance_sheet(symbol):
    res= get_bal_sheet(symbol)
    return jsonify(res)
    

#==========================================================================================
@financials_bp.route('/api/financials/q-cash-flow/<symbol>', methods=['GET'])   
def get_quarterly_cash_flow(symbol):
    res = get_q_cash_flow(symbol)
    return jsonify(res)

@financials_bp.route('/api/financials/cash-flow/<symbol>', methods=['GET'])   
def get_cash_flow(symbol):
    res = get_cash_floww(symbol)
    return jsonify(res)
    