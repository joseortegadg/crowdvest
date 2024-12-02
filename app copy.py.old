import os
import requests
from flask import Flask, jsonify, request, send_from_directory

# Initialize the Flask app
app = Flask(__name__, static_folder='static')

# Alpha Vantage API key
API_KEY = 'XTT9OCEELPXYT4HA'

# Function to fetch SMA data
def fetch_sma(symbol, interval='daily', time_period='20'):
    url = (
        f'https://www.alphavantage.co/query?function=SMA'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&time_period={time_period}'
        f'&series_type=close'
        f'&apikey={API_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: SMA' not in data:
        return None
    sma_data = data['Technical Analysis: SMA']
    latest_date = list(sma_data.keys())[0]
    sma_value = float(sma_data[latest_date]['SMA'])
    return sma_value

# Function to fetch RSI data
def fetch_rsi(symbol, interval='daily', time_period='14'):
    url = (
        f'https://www.alphavantage.co/query?function=RSI'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&time_period={time_period}'
        f'&series_type=close'
        f'&apikey={API_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: RSI' not in data:
        return None
    rsi_data = data['Technical Analysis: RSI']
    latest_date = list(rsi_data.keys())[0]
    rsi_value = float(rsi_data[latest_date]['RSI'])
    return rsi_value

# Function to fetch MACD data
def fetch_macd(symbol, interval='daily'):
    url = (
        f'https://www.alphavantage.co/query?function=MACD'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&apikey={API_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: MACD' not in data:
        return None
    macd_data = data['Technical Analysis: MACD']
    latest_date = list(macd_data.keys())[0]
    macd_value = float(macd_data[latest_date]['MACD'])
    return macd_value

# Function to fetch EMA data
def fetch_ema(symbol, interval='daily', time_period='20'):
    url = (
        f'https://www.alphavantage.co/query?function=EMA'
        f'&symbol={symbol}'
        f'&interval={interval}'
        f'&time_period={time_period}'
        f'&series_type=close'
        f'&apikey={API_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: EMA' not in data:
        return None
    ema_data = data['Technical Analysis: EMA']
    latest_date = list(ema_data.keys())[0]
    ema_value = float(ema_data[latest_date]['EMA'])
    return ema_value

# Serve the index.html file as the front end
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoint to get the consensus for multiple indicators
@app.route('/market/technical/consensus', methods=['GET'])
def get_consensus():
    symbol = request.args.get('symbol')
    interval = request.args.get('interval', 'daily')
    sma_time_period = request.args.get('sma_time_period', '20')
    rsi_time_period = request.args.get('rsi_time_period', '14')
    ema_time_period = request.args.get('ema_time_period', '20')

    consensus = {}

    try:
        # Fetch values for each indicator
        sma_value = fetch_sma(symbol, interval, sma_time_period)
        rsi_value = fetch_rsi(symbol, interval, rsi_time_period)
        macd_value = fetch_macd(symbol, interval)
        ema_value = fetch_ema(symbol, interval, ema_time_period)

        # Add consensus based on each indicator
        if sma_value is not None:
            consensus['SMA'] = "Buy" if sma_value > 100 else "Sell"  # Example logic
        else:
            consensus['SMA'] = "Data not available"

        if rsi_value is not None:
            if rsi_value < 30:
                consensus['RSI'] = "Strong Buy"
            elif rsi_value < 50:
                consensus['RSI'] = "Buy"
            elif rsi_value > 70:
                consensus['RSI'] = "Sell"
            else:
                consensus['RSI'] = "Hold"
        else:
            consensus['RSI'] = "Data not available"

        if macd_value is not None:
            consensus['MACD'] = "Buy" if macd_value > 0 else "Sell"  # Example logic
        else:
            consensus['MACD'] = "Data not available"

        if ema_value is not None:
            consensus['EMA'] = "Buy" if ema_value > 100 else "Sell"  # Example logic
        else:
            consensus['EMA'] = "Data not available"

        return jsonify({
            "symbol": symbol,
            "interval": interval,
            "consensus": consensus
        }), 200

    except Exception as e:
        return jsonify({"msg": f"Error processing request: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
