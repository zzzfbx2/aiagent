import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Simple Financial AI Agent")
st.sidebar.header("Stock Selection")

# User Input
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-12-31"))

if st.sidebar.button("Fetch Data"):
    # Fetch Stock Data
    st.write(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)

    # Display Raw Data
    st.write("### Stock Data", data.tail())

    # Add Technical Indicators
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['Signal'] = 0
    data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1
    data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1

    # Plot Data
    st.write("### Price with Buy/Sell Signals")
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['SMA_20'], label='SMA 20', alpha=0.8)
    plt.plot(data['SMA_50'], label='SMA 50', alpha=0.8)
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green')
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red')
    plt.title(f"Buy/Sell Signals for {ticker}")
    plt.legend()
    st.pyplot(plt)

    # Summary
    st.write("### Signals Summary")
    st.write(f"Buy Signals: {len(buy_signals)}, Sell Signals: {len(sell_signals)}")

# Footer
st.sidebar.info("Simple Financial AI Agent by Raj Deepak")
