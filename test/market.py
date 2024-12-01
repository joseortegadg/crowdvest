# market.py
from flask import Blueprint, request, jsonify
import requests

market_bp = Blueprint('market', __name__)

@market_bp.route('/market/technical/rsi', methods=['GET'])
def get_rsi():
    """
    Get RSI (Relative Strength Index) for a given stock symbol.
    """
    symbol = request.args.get('symbol')
    interval = request.args.get('interval', 'daily')  # Default interval is daily
    time_period = request.args.get('time_period', '14')  # Default time period is 14
    api_key = 'your-alpha-vantage-api-key'

    url = (
        f'https://www.alphavantage.co/query?function=RSI'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&time_period={time_period}'
        f'&series_type=close'
        f'&apikey={api_key}'
    )
    
    response = requests.get(url)
    data = response.json()

    # Handle errors or invalid responses
    if 'Technical Analysis: RSI' not in data:
        return jsonify({"msg": "Error retrieving RSI data"}), 500

    rsi_data = data['Technical Analysis: RSI']
    latest_date = list(rsi_data.keys())[0]  # Get the most recent data
    rsi_value = rsi_data[latest_date]['RSI']

    return jsonify({
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "date": latest_date,
        "rsi": rsi_value
    }), 200



