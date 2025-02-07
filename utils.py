import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol: str):
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        # Get stock info
        stock = yf.Ticker(symbol)

        # Get historical data for the past year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        hist_data = stock.history(start=start_date, end=end_date)

        # Get company info and financial data
        info = stock.info

        # Get news data
        news = stock.news

        # Create metrics dictionary
        metrics = {
            'Current Price': info.get('currentPrice', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            'PE Ratio': info.get('trailingPE', 'N/A'),
            '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
            'Volume': info.get('volume', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A')
        }

        return {
            'metrics': metrics,
            'historical_data': hist_data,
            'news': news,
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def format_large_number(num):
    """
    Format large numbers for better readability
    """
    if not isinstance(num, (int, float)) or pd.isna(num):
        return 'N/A'

    if num >= 1_000_000_000:
        return f'${num/1_000_000_000:.2f}B'
    elif num >= 1_000_000:
        return f'${num/1_000_000:.2f}M'
    elif num >= 1_000:
        return f'${num/1_000:.2f}K'
    else:
        return f'${num:.2f}'

def format_timestamp(timestamp):
    """
    Format Unix timestamp to readable date
    """
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return 'N/A'