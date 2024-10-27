from flask import Blueprint, jsonify
from src.services.stock.calculation.risk_reward import five_year_cagr, five_year_max_drawdown, calculate_volatility, beta_to_ihsg, alpha_to_ihsg
from src.services.stock.basic.stock_info_service import combine_fetched_scraped_info

risk_reward_bp = Blueprint('risk-reward', __name__)

@risk_reward_bp.route('/api/risk-reward/<symbol>/<period>', methods=['GET'])
def get_risk_reward(symbol: str, period:str):
    info = combine_fetched_scraped_info()
    # print(info)

    for i in info:
        if symbol == i['symbol']:
            company_name = i['company_name']

    cagr = five_year_cagr(symbol, period)
    max_drawdown = five_year_max_drawdown(symbol, period)
    volatility = calculate_volatility(symbol, period)
    beta = beta_to_ihsg(symbol, period)
    alpha = alpha_to_ihsg(symbol, period)
    
    res = {
        'symbol': symbol,
        'company_name': company_name,
        'period': period,
        'cagr': cagr,
        'max_drawdown': max_drawdown,
        'volatility': volatility,
        'beta': beta,
        'alpha': alpha,
    }
    return jsonify(res)