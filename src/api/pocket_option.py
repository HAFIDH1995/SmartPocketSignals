import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.models.schemas import CandleData

class PocketOptionAPI:
    """
    محاكي لواجهة برمجة تطبيقات Pocket Option
    في التطبيق الحقيقي، يجب استبدال هذا بالاتصال الفعلي مع Pocket Option
    """
    
    def __init__(self):
        self.connected = False
        self.base_price = 1.1000  # سعر أساسي لـ EURUSD
        
    async def connect(self):
        """الاتصال بـ Pocket Option"""
        # محاكاة الاتصال
        await asyncio.sleep(0.1)
        self.connected = True
        return True
        
    async def disconnect(self):
        """قطع الاتصال"""
        self.connected = False
        
    def _generate_realistic_candle(self, timestamp: datetime, prev_close: float) -> CandleData:
        """توليد شمعة واقعية للاختبار"""
        # تغيير عشوائي صغير في السعر
        change = random.uniform(-0.0020, 0.0020)
        open_price = prev_close
        close_price = open_price + change
        
        # تحديد أعلى وأقل سعر
        high_price = max(open_price, close_price) + random.uniform(0, 0.0010)
        low_price = min(open_price, close_price) - random.uniform(0, 0.0010)
        
        volume = random.uniform(1000, 5000)
        
        return CandleData(
            timestamp=timestamp,
            open=round(open_price, 5),
            high=round(high_price, 5),
            low=round(low_price, 5),
            close=round(close_price, 5),
            volume=volume
        )
        
    async def get_candles(self, asset: str, timeframe: str, count: int = 100) -> List[CandleData]:
        """
        جلب بيانات الشموع
        
        Args:
            asset: اسم الأصل (مثل EURUSD_OTC)
            timeframe: الإطار الزمني (مثل 1m, 5m, 1h)
            count: عدد الشموع المطلوبة
        """
        if not self.connected:
            raise Exception("غير متصل بـ Pocket Option")
            
        # محاكاة تأخير الشبكة
        await asyncio.sleep(0.2)
        
        # تحويل الإطار الزمني إلى دقائق
        timeframe_minutes = self._parse_timeframe(timeframe)
        
        # توليد بيانات الشموع
        candles = []
        current_time = datetime.now()
        current_price = self.base_price
        
        for i in range(count):
            timestamp = current_time - timedelta(minutes=timeframe_minutes * (count - i))
            candle = self._generate_realistic_candle(timestamp, current_price)
            candles.append(candle)
            current_price = candle.close
            
        return candles
        
    def _parse_timeframe(self, timeframe: str) -> int:
        """تحويل الإطار الزمني إلى دقائق"""
        timeframe_map = {
            "5s": 0.083,
            "10s": 0.167,
            "15s": 0.25,
            "30s": 0.5,
            "1m": 1,
            "2m": 2,
            "3m": 3,
            "5m": 5,
            "10m": 10,
            "15m": 15,
            "30m": 30,
            "1h": 60,
            "4h": 240,
            "1d": 1440
        }
        return timeframe_map.get(timeframe, 1)
        
    async def get_current_price(self, asset: str) -> float:
        """جلب السعر الحالي"""
        if not self.connected:
            raise Exception("غير متصل بـ Pocket Option")
            
        # محاكاة تأخير الشبكة
        await asyncio.sleep(0.1)
        
        # إرجاع سعر عشوائي قريب من السعر الأساسي
        variation = random.uniform(-0.0050, 0.0050)
        return round(self.base_price + variation, 5)
        
    def is_otc_asset(self, asset: str) -> bool:
        """فحص ما إذا كان الأصل من نوع OTC"""
        return "OTC" in asset.upper()

# إنشاء مثيل عام للاستخدام
pocket_option_api = PocketOptionAPI()
