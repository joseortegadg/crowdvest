import os
from flask import Flask, jsonify, request, send_from_directory

# Initialize the Flask app
app = Flask(__name__, static_folder='static')

# Serve the index.html file as the front end
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Example endpoint for consensus (SMA + RSI) logic
@app.route('/market/technical/consensus', methods=['GET'])
def get_consensus():
    """
    Get a consensus recommendation (Buy, Sell, Hold) based on SMA and RSI.
    """
    symbol = request.args.get('symbol')
    interval = request.args.get('interval', 'daily')
    sma_time_period = request.args.get('sma_time_period', '20')
    rsi_time_period = request.args.get('rsi_time_period', '14')

    # Example logic for consensus
    sma_value = 100  # You can replace this with actual logic
    rsi_value = 50   # You can replace this with actual logic

    # Consensus logic example
    if rsi_value < 30 and sma_value:  # Oversold
        consensus = "Buy"
    elif rsi_value > 70 and sma_value:  # Overbought
        consensus = "Sell"
    else:
        consensus = "Hold"

    return jsonify({
        "symbol": symbol,
        "interval": interval,
        "sma": sma_value,
        "rsi": rsi_value,
        "consensus": consensus
    }), 200

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
