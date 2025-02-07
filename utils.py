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

        # Get and process news data
        try:
            news = stock.news
            # Clean and validate news data
            processed_news = []
            for article in news:
                if isinstance(article, dict):
                    content = article.get('content', article)
                    processed_article = {
                        'title': content.get('title', ''),
                        'publisher': content.get('provider', {}).get('displayName', 'Unknown'),
                        'link': content.get('canonicalUrl', {}).get('url', '#'),
                        'providerPublishTime': content.get('pubDate', ''),
                        'summary': content.get('summary', '')
                    }
                    if processed_article['title'] and processed_article['summary']:
                        processed_news.append(processed_article)

            print(f"Found {len(processed_news)} news articles for {symbol}")
            if not processed_news:
                print(f"Raw news data for {symbol}: {news[:2]}")
        except Exception as e:
            print(f"Error processing news: {str(e)}")
            processed_news = []

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

        # Calculate price change percentage
        if not hist_data.empty:
            current_price = hist_data['Close'].iloc[-1]
            start_price = hist_data['Close'].iloc[0]
            price_change = ((current_price - start_price) / start_price) * 100
        else:
            price_change = 0

        return {
            'metrics': metrics,
            'historical_data': hist_data,
            'news': processed_news,
            'price_change': price_change,
            'success': True
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
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
        if isinstance(timestamp, str):
            dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        else:
            dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return 'N/A'

def generate_stock_insight_card(symbol: str, data: dict) -> str:
    """
    Generate HTML for a shareable stock insight card with social media sharing
    """
    metrics = data['metrics']
    price_change = data['price_change']
    change_color = 'green' if price_change >= 0 else 'red'

    # Create share text with hashtags and better formatting
    share_text = f"📈 ${symbol} Stock Update:\n• {price_change:+.2f}% change\n• Price: {format_large_number(metrics['Current Price'])}\n• Market Cap: {format_large_number(metrics['Market Cap'])}\n#stocks #investing #finance"

    # Properly encode the share text for URLs
    encoded_text = share_text.replace('\n', '%0A').replace(' ', '%20').replace('#', '%23')

    # Generate social media share URLs with proper parameters
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_text}"
    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_text}"

    card_html = f"""
    <div class="insight-card">
        <div class="card-header">
            <h2>{symbol}</h2>
            <span class="price-change" style="color: {change_color}">
                {price_change:+.2f}%
            </span>
        </div>
        <div class="card-metrics">
            <div class="metric">
                <span class="label">Current Price</span>
                <span class="value">{format_large_number(metrics['Current Price'])}</span>
            </div>
            <div class="metric">
                <span class="label">Market Cap</span>
                <span class="value">{format_large_number(metrics['Market Cap'])}</span>
            </div>
            <div class="metric">
                <span class="label">P/E Ratio</span>
                <span class="value">{metrics['PE Ratio']}</span>
            </div>
        </div>
        <div class="social-share-buttons">
            <a href="{twitter_url}" target="_blank" class="share-button twitter">
                Share on X (Twitter)
            </a>
            <a href="{facebook_url}" target="_blank" class="share-button facebook">
                Share on Facebook
            </a>
            <a href="{linkedin_url}" target="_blank" class="share-button linkedin">
                Share on LinkedIn
            </a>
        </div>
        <div class="card-footer">
            <span class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
        </div>
    </div>
    """
    return card_html