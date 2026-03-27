import pandas as pd
from signals.indicators import TechnicalIndicators

class StrategyEngine:
    def __init__(self):
        self.indicators = TechnicalIndicators()

    def breakout_strategy(self, df):
        """Breakout strategy based on high/low of previous periods."""
        df['high_20'] = df['high'].rolling(window=20).max()
        df['low_20'] = df['low'].rolling(window=20).min()
        
        last_close = df['close'].iloc[-1]
        high_20 = df['high_20'].iloc[-2]
        low_20 = df['low_20'].iloc[-2]
        
        if last_close > high_20:
            return "BUY"
        elif last_close < low_20:
            return "SELL"
        return "HOLD"

    def momentum_strategy(self, df):
        """Momentum strategy based on RSI and MACD."""
        rsi = self.indicators.calculate_rsi(df['close'])
        macd, signal = self.indicators.calculate_macd(df['close'])
        
        last_rsi = rsi.iloc[-1]
        last_macd = macd.iloc[-1]
        last_signal = signal.iloc[-1]
        
        if last_rsi > 50 and last_macd > last_signal:
            return "BUY"
        elif last_rsi < 50 and last_macd < last_signal:
            return "SELL"
        return "HOLD"

    def mean_reversion_strategy(self, df):
        """Mean reversion strategy based on EMA and RSI."""
        ema = self.indicators.calculate_ema(df['close'], period=20)
        rsi = self.indicators.calculate_rsi(df['close'])
        
        last_close = df['close'].iloc[-1]
        last_ema = ema.iloc[-1]
        last_rsi = rsi.iloc[-1]
        
        if last_close < last_ema and last_rsi < 30:
            return "BUY"
        elif last_close > last_ema and last_rsi > 70:
            return "SELL"
        return "HOLD"

    def whale_tracking_strategy(self, df):
        """Whale tracking strategy based on volume spikes."""
        vol_ma = self.indicators.calculate_volume_ma(df['volume'], period=20)
        last_vol = df['volume'].iloc[-1]
        last_vol_ma = vol_ma.iloc[-1]
        
        if last_vol > last_vol_ma * 2:
            # Volume spike detected, check price direction
            if df['close'].iloc[-1] > df['close'].iloc[-2]:
                return "BUY"
            else:
                return "SELL"
        return "HOLD"

    def generate_combined_signal(self, df):
        """Combine all strategies for a final signal."""
        signals = [
            self.breakout_strategy(df),
            self.momentum_strategy(df),
            self.mean_reversion_strategy(df),
            self.whale_tracking_strategy(df)
        ]
        
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        
        if buy_count > sell_count:
            return "BUY"
        elif sell_count > buy_count:
            return "SELL"
        return "HOLD"
