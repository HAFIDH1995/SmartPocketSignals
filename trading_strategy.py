from typing import List, Optional
from pydantic import BaseModel

class CandleData(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: str  # يمكنك استخدام datetime لاحقًا إن أردت

class CandlePattern(BaseModel):
    name: str
    detected: bool
    signal: Optional[str]  # bullish, bearish, or None
    confidence: float  # قيمة بين 0 و 1

class TechnicalIndicator(BaseModel):
    name: str
    value: float
    signal: Optional[str]  # bullish, bearish, or None

class TimeframeAnalysis(BaseModel):
    timeframe: str
    candle_patterns: List[CandlePattern]
    technical_indicators: List[TechnicalIndicator]
    overall_signal: str  # bullish, bearish, or neutral
    score: float

class TradingSignal(BaseModel):
    asset: str
    recommendation: str  # buy, sell, hold
    confidence: float
    trade_details: dict
    analyses: List[TimeframeAnalysis]
