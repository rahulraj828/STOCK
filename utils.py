import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_stock_data(symbol, exchange="NSE"):
    try:
        clean_symbol = symbol.replace(".NS", "").replace(".BO", "")
        if exchange == "NSE":
            return get_yfinance_data(clean_symbol, ".NS", "NSE")
        else:
            return get_yfinance_data(clean_symbol, ".BO", "BSE")
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def get_yfinance_data(symbol, suffix, exchange_name):
    yf_symbol = symbol + suffix
    stock = yf.Ticker(yf_symbol)
    info = stock.info
    hist = stock.history(period="1y")

    if not info or hist.empty:
        raise Exception(f"Invalid data returned for {yf_symbol}")

    return {
        'info': {
            'longName': info.get('longName', symbol),
            'currentPrice': info.get('currentPrice'),
            'previousClose': info.get('previousClose'),
            'regularMarketChangePercent': ((info.get('currentPrice', 0) - info.get('previousClose', 0)) / max(info.get('previousClose', 1), 1)) * 100,
            'marketCap': info.get('marketCap'),
            'volume': info.get('volume'),
            'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh'),
            'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow'),
            'trailingPE': info.get('trailingPE'),
            'dividendYield': info.get('dividendYield'),
            'exchange': exchange_name
        },
        'history': hist,
        'valid': True,
        'exchange': exchange_name
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
        'Volume': format_large_number(info.get('volume')),
    }

@st.cache_data(ttl=300)
def prepare_financial_data(info):
    financial_data = {
        'Revenue': format_large_number(info.get('totalRevenue')),
        'Gross Profit': format_large_number(info.get('grossProfits')),
        'Operating Margin': f"{info.get('operatingMargins', 0) * 100:.2f}%" if info.get('operatingMargins') else "N/A",
        'Return on Equity': f"{info.get('returnOnEquity', 0) * 100:.2f}%" if info.get('returnOnEquity') else "N/A",
        'Debt to Equity': f"{info.get('debtToEquity', 'N/A'):.2f}" if info.get('debtToEquity') else "N/A",
        'Current Ratio': f"{info.get('currentRatio', 'N/A'):.2f}" if info.get('currentRatio') else "N/A",
    }
    return pd.DataFrame(list(financial_data.items()), columns=['Metric', 'Value'])
