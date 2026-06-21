import yfinance as yf
import streamlit as st
@st.cache_data(ttl=60)
def get_stock_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    return stock.history(period=period)
@st.cache_data(ttl=60)
def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info