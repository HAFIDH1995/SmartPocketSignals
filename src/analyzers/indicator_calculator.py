import numpy as np
from typing import List
from src.models.schemas import CandleData, TechnicalIndicator

class TechnicalIndicatorCalculator:
    """حاسبة المؤشرات الفنية"""
    
    def __init__(self):
        self.indicators = {
            "rsi": {"weight": 15, "description": "مؤشر القوة النسبية"},
            "macd": {"weight": 20, "description": "مؤشر MACD"},
            "bollinger_bands": {"weight": 15, "description": "نطاقات بولينجر"},
            "ema_cross": {"weight": 10, "description": "تقاطع المتوسطات المتحركة"},
            "stochastic": {"weight": 10, "description": "مؤشر ستوكاستيك"}
        }
    
    def calculate_all_indicators(self, candles: List[CandleData]) -> List[TechnicalIndicator]:
        """حساب جميع المؤشرات الفنية"""
        if len(candles) < 20:
            return []
        
        indicators = []
        prices = [candle.close for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        
        rsi_indicator = self._calculate_rsi(prices)
        if rsi_indicator:
            indicators.append(rsi_indicator)

        macd_indicator = self._calculate_macd(prices)
        if macd_indicator:
            indicators.append(macd_indicator)

        bb_indicator = self._calculate_bollinger_bands(prices)
        if bb_indicator:
            indicators.append(bb_indicator)

        ema_indicator = self._calculate_ema_cross(prices)
        if ema_indicator:
            indicators.append(ema_indicator)

        stoch_indicator = self._calculate_stochastic(highs, lows, prices)
        if stoch_indicator:
            indicators.append(stoch_indicator)

        return indicators

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> TechnicalIndicator:
        if len(prices) < period + 1:
            return None
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        rsi = 100 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))
        signal = "bullish" if rsi < 30 else "bearish" if rsi > 70 else "neutral"

        return TechnicalIndicator(
            name="rsi",
            value=round(rsi, 2),
            signal=signal,
            weight=self.indicators["rsi"]["weight"]
        )

    def _calculate_macd(self, prices: List[float]) -> TechnicalIndicator:
        if len(prices) < 26:
            return None

        prices_array = np.array(prices)
        ema_12 = self._calculate_ema(prices_array, 12)
        ema_26 = self._calculate_ema(prices_array, 26)

        macd_line = ema_12[-1] - ema_26[-1]
        macd_values = ema_12 - ema_26
        signal_line = self._calculate_ema(macd_values, 9)[-1]

        if macd_line > signal_line and macd_line > 0:
            signal = "bullish"
        elif macd_line < signal_line and macd_line < 0:
            signal = "bearish"
        else:
            signal = "neutral"

        return TechnicalIndicator(
            name="macd",
            value=round(macd_line, 5),
            signal=signal,
            weight=self.indicators["macd"]["weight"]
        )

    def _calculate_bollinger_bands(self, prices: List[float], period: int = 20) -> TechnicalIndicator:
        if len(prices) < period:
            return None

        prices_array = np.array(prices[-period:])
        sma = np.mean(prices_array)
        std = np.std(prices_array)

        upper_band = sma + 2 * std
        lower_band = sma - 2 * std
        current_price = prices[-1]

        if current_price > upper_band:
            signal = "bearish"
        elif current_price < lower_band:
            signal = "bullish"
        else:
            signal = "neutral"

        bb_position = (current_price - lower_band) / (upper_band - lower_band)

        return TechnicalIndicator(
            name="bollinger_bands",
            value=round(bb_position, 3),
            signal=signal,
            weight=self.indicators["bollinger_bands"]["weight"]
        )

    def _calculate_ema_cross(self, prices: List[float]) -> TechnicalIndicator:
        if len(prices) < 50:
            return None

        prices_array = np.array(prices)
        ema_20 = self._calculate_ema(prices_array, 20)
        ema_50 = self._calculate_ema(prices_array, 50)

        current_diff = ema_20[-1] - ema_50[-1]
        prev_diff = ema_20[-2] - ema_50[-2] if len(ema_20) > 1 else 0

        if current_diff > 0 and prev_diff <= 0:
            signal = "bullish"
        elif current_diff < 0 and prev_diff >= 0:
            signal = "bearish"
        elif current_diff > 0:
            signal = "bullish"
        elif current_diff < 0:
            signal = "bearish"
        else:
            signal = "neutral"

        return TechnicalIndicator(
            name="ema_cross",
            value=round(current_diff, 5),
            signal=signal,
            weight=self.indicators["ema_cross"]["weight"]
        )

    def _calculate_stochastic(self, highs: List[float], lows: List[float], closes: List[float], k_period: int = 14) -> TechnicalIndicator:
        if len(closes) < k_period:
            return None

        recent_highs = highs[-k_period:]
        recent_lows = lows[-k_period:]
        current_close = closes[-1]

        highest_high = max(recent_highs)
        lowest_low = min(recent_lows)

        k_percent = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100 if highest_high != lowest_low else 50
        signal = "bullish" if k_percent < 20 else "bearish" if k_percent > 80 else "neutral"

        return TechnicalIndicator(
            name="stochastic",
            value=round(k_percent, 2),
            signal=signal,
            weight=self.indicators["stochastic"]["weight"]
        )

    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        alpha = 2 / (period + 1)
        ema = np.zeros_like(prices)
        ema[0] = prices[0]
        for i in range(1, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
        return ema
