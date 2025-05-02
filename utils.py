import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=300)
def get_stock_data(symbol, exchange="NSE"):
    """Fetch stock data from NSE or BSE using yfinance."""
    try:
        clean_symbol = symbol.replace(".NS", "").replace(".BO", "")
        suffix = ".NS" if exchange == "NSE" else ".BO"
        yf_symbol = f"{clean_symbol}{suffix}"

        stock = yf.Ticker(yf_symbol)
        info = stock.info
        hist = stock.history(period="1y")

        if not info or hist.empty:
            raise ValueError(f"Invalid data returned for {yf_symbol}")

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")

        info_data = {
            "longName": info.get("longName", clean_symbol),
            "currentPrice": current_price,
            "previousClose": info.get("previousClose"),
            "regularMarketChangePercent": info.get("regularMarketChangePercent", 0),
            "marketCap": info.get("marketCap"),
            "volume": info.get("volume"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "trailingPE": info.get("trailingPE"),
            "dividendYield": info.get("dividendYield"),
            "exchange": exchange
        }

        return {
            "info": info_data,
            "history": hist,
            "valid": True,
            "exchange": exchange
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }

@st.cache_data(ttl=3600)
def format_large_number(num):
    if num is None:
        return "N/A"
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])

@st.cache_data(ttl=300)
def prepare_metrics_data(info):
    return {
        'Market Cap': format_large_number(info.get('marketCap')),
        'PE Ratio': f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "N/A",
        'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A",
        '52 Week High': f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}",
        '52 Week Low': f"₹{info.get('fiftyTwoWeekLow', 'N/A')}",
        'Volume': format_large_number(info.get('volume'))
    }

@st.cache_data(ttl=300)
def prepare_financial_data(info):
    financial_data = {
        'Market Cap': format_large_number(info.get('marketCap')),
        'PE Ratio': f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "N/A",
        'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A",
        '52 Week High': f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}",
        '52 Week Low': f"₹{info.get('fiftyTwoWeekLow', 'N/A')}",
        'Current Price': f"₹{info.get('currentPrice', 'N/A')}",
        'Previous Close': f"₹{info.get('previousClose', 'N/A')}"
    }
    return pd.DataFrame(list(financial_data.items()), columns=['Metric', 'Value'])
