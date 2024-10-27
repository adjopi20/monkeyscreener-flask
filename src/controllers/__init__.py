from src.controllers.basic.stock_actions import actions_bp
from src.controllers.basic.stock_history import history_bp
from src.controllers.basic.stock_info_controller import info_bp
from src.controllers.basic.stock_financials import financials_bp
from src.controllers.basic.stock_holders import holders_bp
from src.controllers.basic.stock_recommendations import recommendations_bp
from src.controllers.basic.stock_news import news_bp
from src.controllers.analysis.histogram_per_sector_controller import hist_bp
from src.controllers.analysis.risk_reward import risk_reward_bp


blueprints = [
    info_bp,
    history_bp,
    actions_bp,
    financials_bp,
    holders_bp,
    recommendations_bp,
    news_bp,
    hist_bp,
    risk_reward_bp,
]