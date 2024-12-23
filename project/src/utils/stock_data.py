import yfinance as yf
import pandas as pd
from datetime import datetime

def get_stock_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.Series:
    """Fetch historical stock data from Yahoo Finance"""
    if not ticker.endswith('.SA'):
        ticker = f"{ticker}.SA"
    try:
        stock = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        return stock['High']
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker}: {str(e)}")