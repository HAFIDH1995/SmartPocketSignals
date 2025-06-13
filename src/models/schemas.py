from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CandleData(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None

class TechnicalIndicator(BaseModel):
    name: str
    value: float
    signal: str
    weight: int

class CandlePattern(BaseModel):
    name: str
    detected: bool
    signal: str
    weight: int
    confidence: float

class TimeframeAnalysis(BaseModel):
    timeframe: str
    candle_patterns: List[CandlePattern]
    technical_indicators: List[TechnicalIndicator]
    overall_signal: str
    score: float

class AIResponse(BaseModel):
    provider: str
    approval: bool
    confidence: float
    reasoning: str

class TradingSignal(BaseModel):
    asset: str
    recommendation: str
    entry_time: datetime
    trade_duration: str
    target_price: Optional[float]
    technical_confidence: float
    ai_confidence: float
    final_confidence: float
    timeframe_analyses: List[TimeframeAnalysis]
    ai_responses: List[AIResponse]
    created_at: datetime
