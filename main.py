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
st.markdown("Enter stock symbols to compare multiple stocks' data and performance.")

# Input for stock symbols
symbols_input = st.text_input(
    "Enter Stock Symbols (comma-separated, e.g., AAPL, GOOGL, MSFT)", 
    ""
).upper()

if symbols_input:
    # Split and clean input
    symbols = [sym.strip() for sym in symbols_input.split(',') if sym.strip()]

    if len(symbols) > 0:
        with st.spinner('Fetching stock data...'):
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📊 Price Comparison", "📰 News Feed"])

            with tab1:
                # Initialize the comparison chart
                fig = go.Figure()
                comparison_data = {}

                # Fetch data for each symbol
                for symbol in symbols:
                    data = get_stock_data(symbol)
                    if data['success']:
                        comparison_data[symbol] = data
                        hist_data = data['historical_data']

                        # Normalize prices to percentage change
                        first_close = hist_data['Close'].iloc[0]
                        normalized_prices = ((hist_data['Close'] - first_close) / first_close) * 100

                        fig.add_trace(go.Scatter(
                            x=hist_data.index,
                            y=normalized_prices,
                            name=symbol,
                            mode='lines'
                        ))

                fig.update_layout(
                    title='Stock Price Comparison (% Change)',
                    yaxis_title='Price Change (%)',
                    xaxis_title='Date',
                    template='plotly_white',
                    height=500,
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

                # Comparison metrics table
                st.subheader("Key Metrics Comparison")
                metrics_comparison = {}

                for symbol, data in comparison_data.items():
                    metrics_comparison[symbol] = data['metrics']

                # Convert to DataFrame for easy comparison
                metrics_df = pd.DataFrame(metrics_comparison)

                # Format all numeric values
                for col in metrics_df.columns:
                    metrics_df[col] = metrics_df[col].apply(
                        lambda x: format_large_number(x) if isinstance(x, (int, float)) else x
                    )

                st.table(metrics_df)

            with tab2:
                # News feed for each stock
                for symbol in symbols:
                    if symbol in comparison_data:
                        st.subheader(f"📰 Latest News - {symbol}")
                        news_data = comparison_data[symbol]['news']

                        if news_data:
                            for article in news_data[:3]:  # Display top 3 news articles per stock
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
                            st.info(f"No recent news articles available for {symbol}")

                # Download button for CSV
                st.subheader("Download Data")
                for symbol, data in comparison_data.items():
                    csv_data = data['historical_data'].reset_index()
                    csv = csv_data.to_csv(index=False)
                    st.download_button(
                        label=f"Download {symbol} Historical Data (CSV)",
                        data=csv,
                        file_name=f"{symbol}_historical_data.csv",
                        mime="text/csv",
                    )
    else:
        st.warning("Please enter at least one valid stock symbol.")
else:
    st.info("👆 Enter one or more stock symbols above to get started!")

# Footer
st.markdown("---")
st.markdown(
    "Data provided by Yahoo Finance. Built with Streamlit, yfinance, and Plotly."
)