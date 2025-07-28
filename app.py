import streamlit as st
from utils import fetch_stock_data, get_summary_from_chatgpt, get_top_movers

st.set_page_config(page_title="TrendSmart", layout="centered")

st.title("📈 TrendSmart – AI Stock Picks")

menu = st.sidebar.selectbox("Navigate", ["📊 Stock Summary", "🚀 Trending", "⭐ Watchlist"])

if menu == "📊 Stock Summary":
    ticker = st.text_input("Enter Stock Ticker:", value="AAPL").upper()
    if st.button("Analyze"):
        data = fetch_stock_data(ticker)
        if not data.empty:
            summary = get_summary_from_chatgpt(ticker, data)
            st.success(summary)
            if st.button("⭐ Add to Watchlist"):
                with open("watchlist.txt", "a") as f:
                    f.write(f"{ticker}\n")
                st.toast(f"{ticker} added to watchlist!")
        else:
            st.error("Couldn't retrieve data for that ticker.")

elif menu == "🚀 Trending":
    st.subheader("Top Movers This Week")
    movers = get_top_movers()
    for ticker, change in movers:
        st.metric(label=f"{ticker}", value=f"{change:.2f}%", delta=f"{change:.2f}%")

elif menu == "⭐ Watchlist":
    st.subheader("Your Watchlist")
    try:
        with open("watchlist.txt", "r") as f:
            tickers = set(line.strip() for line in f if line.strip())
        if tickers:
            for ticker in tickers:
                data = fetch_stock_data(ticker)
                if not data.empty:
                    summary = get_summary_from_chatgpt(ticker, data)
                    st.markdown(f"**{ticker}** — {summary}")
        else:
            st.info("Watchlist is empty.")
    except FileNotFoundError:
        st.info("Watchlist not yet created.")
