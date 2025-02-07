import streamlit as st
import plotly.graph_objects as go
from utils import get_stock_data, format_large_number, format_timestamp
from styles import STYLES
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Stock Data Visualization",
    page_icon="📈",
    layout="wide"
)

# Apply custom styles
st.markdown(STYLES, unsafe_allow_html=True)

# Title and description
st.title("📈 Stock Data Visualization")
st.markdown("Enter a stock symbol to view its financial data, historical price chart, and latest news.")

# Input for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL)", "").upper()

if symbol:
    with st.spinner('Fetching stock data...'):
        data = get_stock_data(symbol)

        if data['success']:
            # Create two columns for layout
            col1, col2 = st.columns([2, 1])

            with col1:
                # Plot stock price chart
                fig = go.Figure()
                hist_data = data['historical_data']

                fig.add_trace(go.Candlestick(
                    x=hist_data.index,
                    open=hist_data['Open'],
                    high=hist_data['High'],
                    low=hist_data['Low'],
                    close=hist_data['Close'],
                    name='Price'
                ))

                fig.update_layout(
                    title=f'{symbol} Stock Price - Past Year',
                    yaxis_title='Price (USD)',
                    xaxis_title='Date',
                    template='plotly_white',
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)

                # News Feed Section
                st.subheader("📰 Latest News")
                news_data = data['news']

                if news_data:
                    for article in news_data[:5]:  # Display top 5 news articles
                        with st.container():
                            st.markdown(f"""
                            <div class="news-card">
                                <div class="news-title">{article['title']}</div>
                                <div class="news-meta">
                                    {format_timestamp(article['providerPublishTime'])} | 
                                    Source: {article['publisher']}
                                </div>
                                <div class="news-summary">{article['summary']}</div>
                                <a href="{article['link']}" target="_blank">Read more</a>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No recent news articles available for this stock.")

            with col2:
                # Display metrics in a table
                st.subheader("Key Metrics")
                metrics_df = pd.DataFrame.from_dict(
                    data['metrics'],
                    orient='index',
                    columns=['Value']
                )

                # Format the values
                metrics_df['Value'] = metrics_df['Value'].apply(
                    lambda x: format_large_number(x) if isinstance(x, (int, float)) else x
                )

                st.table(metrics_df)

                # Download button for CSV
                csv_data = data['historical_data'].reset_index()
                csv = csv_data.to_csv(index=False)
                st.download_button(
                    label="Download Historical Data (CSV)",
                    data=csv,
                    file_name=f"{symbol}_historical_data.csv",
                    mime="text/csv",
                )

        else:
            st.error(f"Error fetching data: {data['error']}")
            st.markdown("""
                Please check if:
                - The stock symbol is correct
                - You have a working internet connection
                - The Yahoo Finance API is accessible
            """)
else:
    st.info("👆 Enter a stock symbol above to get started!")

# Footer
st.markdown("---")
st.markdown(
    "Data provided by Yahoo Finance. Built with Streamlit, yfinance, and Plotly."
)