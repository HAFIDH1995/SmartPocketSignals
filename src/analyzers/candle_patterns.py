from typing import List, Optional
from src.models.schemas import CandleData, CandlePattern

class CandlePatternAnalyzer:
    """محلل نماذج الشموع"""
    
    def __init__(self):
        self.patterns = {
            "hammer": {"weight": 8, "description": "نموذج المطرقة"},
            "doji": {"weight": 6, "description": "نموذج الدوجي"},
            "engulfing": {"weight": 10, "description": "نموذج الابتلاع"},
            "shooting_star": {"weight": 6, "description": "نموذج النجم الساقط"},
            "spinning_top": {"weight": 4, "description": "نموذج القمة الدوارة"}
        }
    
    def analyze_patterns(self, candles: List[CandleData]) -> List[CandlePattern]:
        """تحليل نماذج الشموع"""
        if len(candles) < 2:
            return []
            
        patterns = []
        
        # تحليل الشمعة الأخيرة والسابقة
        current = candles[-1]
        previous = candles[-2] if len(candles) > 1 else None
        
        # فحص نموذج المطرقة
        hammer_pattern = self._detect_hammer(current)
        if hammer_pattern:
            patterns.append(hammer_pattern)
            
        # فحص نموذج الدوجي
        doji_pattern = self._detect_doji(current)
        if doji_pattern:
            patterns.append(doji_pattern)
            
        # فحص نموذج الابتلاع (يحتاج شمعتين)
        if previous:
            engulfing_pattern = self._detect_engulfing(previous, current)
            if engulfing_pattern:
                patterns.append(engulfing_pattern)
                
        # فحص نموذج النجم الساقط
        shooting_star_pattern = self._detect_shooting_star(current)
        if shooting_star_pattern:
            patterns.append(shooting_star_pattern)
            
        return patterns
    
    def _detect_hammer(self, candle: CandleData) -> Optional[CandlePattern]:
        """كشف نموذج المطرقة"""
        body_size = abs(candle.close - candle.open)
        total_range = candle.high - candle.low
        lower_shadow = min(candle.open, candle.close) - candle.low
        upper_shadow = candle.high - max(candle.open, candle.close)
        
        if (total_range > 0 and 
            body_size / total_range < 0.3 and
            lower_shadow / total_range > 0.6 and
            upper_shadow / total_range < 0.1):
            
            return CandlePattern(
                name="hammer",
                detected=True,
                signal="bullish",
                weight=self.patterns["hammer"]["weight"],
                confidence=0.8
            )
        return None
    
    def _detect_doji(self, candle: CandleData) -> Optional[CandlePattern]:
        """كشف نموذج الدوجي"""
        body_size = abs(candle.close - candle.open)
        total_range = candle.high - candle.low
        
        if total_range > 0 and body_size / total_range < 0.1:
            return CandlePattern(
                name="doji",
                detected=True,
                signal="neutral",
                weight=self.patterns["doji"]["weight"],
                confidence=0.7
            )
        return None
    
    def _detect_engulfing(self, prev_candle: CandleData, current_candle: CandleData) -> Optional[CandlePattern]:
        """كشف نموذج الابتلاع"""
        prev_bullish = prev_candle.close > prev_candle.open
        current_bullish = current_candle.close > current_candle.open
        
        if (not prev_bullish and current_bullish and
            current_candle.open < prev_candle.close and
            current_candle.close > prev_candle.open):
            
            return CandlePattern(
                name="engulfing",
                detected=True,
                signal="bullish",
                weight=self.patterns["engulfing"]["weight"],
                confidence=0.9
            )
        elif (prev_bullish and not current_bullish and
              current_candle.open > prev_candle.close and
              current_candle.close < prev_candle.open):
            
            return CandlePattern(
                name="engulfing",
                detected=True,
                signal="bearish",
                weight=self.patterns["engulfing"]["weight"],
                confidence=0.9
            )
        return None
    
    def _detect_shooting_star(self, candle: CandleData) -> Optional[CandlePattern]:
        """كشف نموذج النجم الساقط"""
        body_size = abs(candle.close - candle.open)
        total_range = candle.high - candle.low
        lower_shadow = min(candle.open, candle.close) - candle.low
        upper_shadow = candle.high - max(candle.open, candle.close)
        
        if (total_range > 0 and 
            body_size / total_range < 0.3 and
            upper_shadow / total_range > 0.6 and
            lower_shadow / total_range < 0.1):
            
            return CandlePattern(
                name="shooting_star",
                detected=True,
                signal="bearish",
                weight=self.patterns["shooting_star"]["weight"],
                confidence=0.8
            )
        return None
