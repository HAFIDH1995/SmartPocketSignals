from typing import List, Optional, Dict, Any
from src.models.schemas import CandleData, CandlePattern, TechnicalIndicator, TimeframeAnalysis, TradingSignal

class TradingStrategy:
    """استراتيجية التداول لتوليد الإشارات"""

    def __init__(self):
        self.timeframe_weights = {
            '1m': 0.1,
            '5m': 0.2,
            '15m': 0.3,
            '30m': 0.2,
            '1h': 0.2
        }

    def analyze_timeframe(self, timeframe: str, candle_patterns: List[CandlePattern], technical_indicators: List[TechnicalIndicator]) -> TimeframeAnalysis:
        """تحليل إطار زمني محدد وتحديد الإشارة الكلية"""
        bullish_score = 0
        bearish_score = 0

        # تقييم نماذج الشموع
        for pattern in candle_patterns:
            if pattern.detected:
                if pattern.signal == "bullish":
                    bullish_score += pattern.weight * pattern.confidence
                elif pattern.signal == "bearish":
                    bearish_score += pattern.weight * pattern.confidence

        # تقييم المؤشرات الفنية
        for indicator in technical_indicators:
            if indicator.signal == "bullish":
                bullish_score += indicator.weight
            elif indicator.signal == "bearish":
                bearish_score += indicator.weight

        overall_signal = "neutral"
        if bullish_score > bearish_score:
            overall_signal = "bullish"
        elif bearish_score > bullish_score:
            overall_signal = "bearish"

        total_score = bullish_score - bearish_score

        return TimeframeAnalysis(
            timeframe=timeframe,
            candle_patterns=candle_patterns,
            technical_indicators=technical_indicators,
            overall_signal=overall_signal,
            score=total_score
        )

    def generate_signal(self, timeframe_analyses: List[TimeframeAnalysis], asset: str) -> Dict[str, Any]:
        """توليد إشارة تداول بناءً على تحليلات الأطر الزمنية"""
        weighted_bullish_score = 0
        weighted_bearish_score = 0
        total_weight = 0

        for analysis in timeframe_analyses:
            weight = self.timeframe_weights.get(analysis.timeframe, 0)
            total_weight += weight

            if analysis.overall_signal == "bullish":
                weighted_bullish_score += analysis.score * weight
            elif analysis.overall_signal == "bearish":
                weighted_bearish_score += analysis.score * weight

        recommendation = "hold"
        technical_confidence = 0.0

        if total_weight > 0:
            final_score = (weighted_bullish_score - weighted_bearish_score) / total_weight
            technical_confidence = abs(final_score) * 100

            if final_score > 0.1:  # عتبة قابلة للتعديل
                recommendation = "buy"
            elif final_score < -0.1:  # عتبة قابلة للتعديل
                recommendation = "sell"

        # تفاصيل التداول (مثال)
        trade_details = {
            "entry_time": None,  # سيتم تحديده لاحقًا
            "duration": "5m",  # مثال: 5 دقائق
            "target_price": None  # سيتم تحديده لاحقًا
        }

        return recommendation, technical_confidence, trade_details


