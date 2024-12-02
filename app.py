import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Alpha Vantage API key
API_KEY = 'XTT9OCEELPXYT4HA'

# Example list of top 5 most moving stocks (you can change this to be dynamic or based on an external source)
top_stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Function to fetch technical indicators (SMA, RSI, etc.)
def fetch_sma(symbol, interval='daily', time_period='20'):
    url = f'https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: SMA' not in data:
        return None
    sma_data = data['Technical Analysis: SMA']
    latest_date = list(sma_data.keys())[0]
    return float(sma_data[latest_date]['SMA'])

def fetch_rsi(symbol, interval='daily', time_period='14'):
    url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: RSI' not in data:
        return None
    rsi_data = data['Technical Analysis: RSI']
    latest_date = list(rsi_data.keys())[0]
    return float(rsi_data[latest_date]['RSI'])

def fetch_macd(symbol, interval='daily'):
    url = f'https://www.alphavantage.co/query?function=MACD&symbol={symbol}&interval={interval}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: MACD' not in data:
        return None
    macd_data = data['Technical Analysis: MACD']
    latest_date = list(macd_data.keys())[0]
    macd_value = float(macd_data[latest_date]['MACD'])
    return macd_value

def fetch_ema(symbol, interval='daily', time_period='20'):
    url = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Technical Analysis: EMA' not in data:
        return None
    ema_data = data['Technical Analysis: EMA']
    latest_date = list(ema_data.keys())[0]
    return float(ema_data[latest_date]['EMA'])

def fetch_sentiment(symbol):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'feed' not in data:
        return None
    sentiment_scores = [article['sentiment_score'] for article in data['feed']]
    if sentiment_scores:
        return sum(sentiment_scores) / len(sentiment_scores)
    return None

# Consensus logic based on technical indicators
def get_consensus(sma, rsi, macd, ema):
    consensus = {}
    
    if sma is not None:
        consensus['SMA'] = "Buy" if sma < 50 else "Sell"
    else:
        consensus['SMA'] = "Data not available"
    
    if rsi is not None:
        if rsi < 30:
            consensus['RSI'] = "Buy"
        elif rsi > 70:
            consensus['RSI'] = "Sell"
        else:
            consensus['RSI'] = "Hold"
    else:
        consensus['RSI'] = "Data not available"
    
    if macd is not None:
        consensus['MACD'] = "Buy" if macd > 0 else "Sell"
    else:
        consensus['MACD'] = "Data not available"
    
    if ema is not None:
        consensus['EMA'] = "Buy" if ema < 50 else "Sell"
    else:
        consensus['EMA'] = "Data not available"
    
    return consensus


@app.route('/')
def index():
    stock_data = []
    
    # Debugging: Print expert forecasts to verify it's populated
    print("Expert Forecasts:", expert_forecasts)
    
    for symbol in top_stocks:
        sma = fetch_sma(symbol)
        rsi = fetch_rsi(symbol)
        macd = fetch_macd(symbol)
        ema = fetch_ema(symbol)
        sentiment_score = fetch_sentiment(symbol)
        
        consensus = get_consensus(sma, rsi, macd, ema)
        
        stock_data.append({
            'symbol': symbol,
            'sma': sma,
            'rsi': rsi,
            'macd': macd,
            'ema': ema,
            'sentiment_score': sentiment_score,
            'consensus': consensus
        })
    
    return render_template('index.html', stock_data=stock_data, expert_forecasts=expert_forecasts)



@app.route('/stock/<symbol>')
def stock(symbol):
    sma = fetch_sma(symbol)
    rsi = fetch_rsi(symbol)
    macd = fetch_macd(symbol)
    ema = fetch_ema(symbol)
    sentiment_score = fetch_sentiment(symbol)
    
    consensus = get_consensus(sma, rsi, macd, ema)
    
    stock_data = {
        'symbol': symbol,
        'sma': sma,
        'rsi': rsi,
        'macd': macd,
        'ema': ema,
        'sentiment_score': sentiment_score,
        'consensus': consensus
    }

    return render_template('stock.html', stock_data=stock_data, expert_forecasts=expert_forecasts)


from flask import request, redirect, url_for

# New route to handle expert forecast submissions
@app.route('/forecast/<symbol>', methods=['GET', 'POST'])
def forecast(symbol):
    if request.method == 'POST':
        price_target = request.form['price_target']
        recommendation = request.form['recommendation']
        rationale = request.form['rationale']
        
        # Add the forecast to expert_forecasts
        if symbol not in expert_forecasts:
            expert_forecasts[symbol] = []
        
        expert_forecasts[symbol].append({
            'price_target': price_target,
            'recommendation': recommendation,
            'rationale': rationale
        })

        # Debugging: Print the updated expert forecasts
        print(f"Expert Forecasts for {symbol}: {expert_forecasts[symbol]}")
        
        return redirect(url_for('stock', symbol=symbol))
    
    return render_template('forecast.html', symbol=symbol)


# In-memory storage for expert forecasts (This can be replaced with a database in production)
expert_forecasts = {}



if __name__ == '__main__':
    app.run(debug=True)