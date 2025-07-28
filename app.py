import streamlit as st
from utils import fetch_stock_data, get_summary_from_chatgpt, get_top_movers

st.set_page_config(page_title="TrendSmart AI", layout="centered")

st.title("📈 TrendSmart – AI Stock Picks")

menu = st.sidebar.selectbox("Navigate", ["📊 Stock Summary", "🚀 Trending", "⭐ Watchlist", "💸 Go Premium"])

if menu == "📊 Stock Summary":
    st.caption("Free users can analyze 1 stock per day.")
    ticker = st.text_input("Enter Stock Ticker (Free Tier)", value="AAPL").upper()
    if st.button("Analyze"):
        data = fetch_stock_data(ticker)
        if not data.empty:
            summary = get_summary_from_chatgpt(ticker, data)
            st.success(summary)

elif menu == "🚀 Trending":
    st.subheader("Top Movers This Week (Free)")
    movers = get_top_movers()
    for ticker, change in movers[:5]:
        st.metric(label=f"{ticker}", value=f"{change:.2f}%", delta=f"{change:.2f}%")

elif menu == "⭐ Watchlist":
    st.info("🔒 Watchlist feature available in Premium only.")
    st.markdown("➡ [Upgrade here](https://trendsmartai.substack.com/subscribe)")

elif menu == "💸 Go Premium":
    st.header("🚀 Unlock Premium Features")
    st.markdown("""
    - ✅ Analyze up to **10 stocks/day**
    - ✅ Get **weekly AI-powered picks** to your inbox
    - ✅ Unlock your **Watchlist** and advanced alerts  
      
    👉 [**Subscribe to TrendSmart Premium**](https://trendsmartai.substack.com/subscribe)
    """)
