import yfinance as yf
import openai
import datetime

openai.api_key = 'YOUR_OPENAI_API_KEY'

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=14)
    hist = stock.history(start=start, end=end)
    return hist

def get_summary_from_chatgpt(ticker, data):
    change = (data['Close'][-1] - data['Close'][0]) / data['Close'][0] * 100
    latest_price = data['Close'][-1]
    prompt = f"""
    Analyze the stock {ticker}. The current price is ${latest_price:.2f}.
    It changed by {change:.2f}% over the past 14 days.
    Provide a short, investor-friendly summary of the trend and outlook.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def get_top_movers():
    tickers = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'AMZN', 'META']
    movers = []
    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if not data.empty:
            change = (data['Close'][-1] - data['Close'][0]) / data['Close'][0] * 100
            movers.append((ticker, change))
    movers.sort(key=lambda x: x[1], reverse=True)
    return movers
