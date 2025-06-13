from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MarketData(BaseModel):
    """نموذج بيانات السوق"""
    asset: str
    timeframe: str
    candles: List[Dict]  # قائمة الشموع
    last_update: datetime

class AnalysisRequest(BaseModel):
    """نموذج طلب التحليل"""
    asset: Optional[str] = "EURUSD_OTC"
    timeframes: Optional[List[str]] = None

class AnalysisResult(BaseModel):
    """نموذج نتيجة التحليل"""
    success: bool
    message: str
    signal: Optional[Dict] = None
    error: Optional[str] = None
