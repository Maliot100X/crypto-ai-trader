import pandas as pd
import numpy as np

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_macd(prices, slow=26, fast=12, signal=9):
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    @staticmethod
    def calculate_ema(prices, period=20):
        return prices.ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_vwap(df):
        q = df['volume']
        p = (df['high'] + df['low'] + df['close']) / 3
        return (p * q).cumsum() / q.cumsum()

    @staticmethod
    def calculate_volume_ma(volume, period=20):
        return volume.rolling(window=period).mean()
