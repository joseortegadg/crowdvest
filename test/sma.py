from flask import Blueprint, request, jsonify
import requests

# Create a Blueprint for the SMA API
sma_bp = Blueprint('sma', __name__)

@sma_bp.route('/market/technical/sma', methods=['GET'])
def get_sma():
    """
    Get SMA (Simple Moving Average) for a given stock symbol.
    """
    symbol = request.args.get('symbol')
    interval = request.args.get('interval', 'daily')  # Default interval is daily
    time_period = request.args.get('time_period', '20')  # Default time period is 20
    api_key = 'your-alpha-vantage-api-key'

    url = (
        f'https://www.alphavantage.co/query?function=SMA'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&time_period={time_period}'
        f'&series_type=close'
        f'&apikey={api_key}'
    )

    response = requests.get(url)
    data = response.json()

    # Handle errors or invalid responses
    if 'Technical Analysis: SMA' not in data:
        return jsonify({"msg": "Error retrieving SMA data"}), 500

    sma_data = data['Technical Analysis: SMA']
    latest_date = list(sma_data.keys())[0]  # Get the most recent data
    sma_value = sma_data[latest_date]['SMA']

    return jsonify({
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "date": latest_date,
        "sma": sma_value
    }), 200

