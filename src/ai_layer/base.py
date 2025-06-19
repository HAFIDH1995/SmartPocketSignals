from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.schemas import AIResponse

class BaseAIHandler(ABC):
    """الفئة الأساسية لمعالجات الذكاء الاصطناعي"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.api_key = None

    @abstractmethod
    async def analyze_signal(self, signal_data: Dict[str, Any]) -> AIResponse:
        """تحليل الإشارة باستخدام الذكاء الاصطناعي"""
        pass

    def create_prompt(self, signal_data: Dict[str, Any]) -> str:
        """إنشاء النص المطلوب للذكاء الاصطناعي"""
        asset = signal_data.get('asset', 'غير محدد')
        recommendation = signal_data.get('recommendation', 'غير محدد')
        technical_confidence = signal_data.get('technical_confidence', 0)

        # تفاصيل التحليل الفني
        candle_patterns = signal_data.get('candle_patterns', [])
        technical_indicators = signal_data.get('technical_indicators', [])

        # تنسيق نماذج الشموع
        patterns_text = ""
        if candle_patterns:
            patterns_text = "\n".join([
                f"- {pattern['name']}: {pattern['signal']} (ثقة: {pattern['confidence']})"
                for pattern in candle_patterns if pattern['detected']
            ])

        # تنسيق المؤشرات الفنية
        indicators_text = ""
        if technical_indicators:
            indicators_text = "\n".join([
                f"- {indicator['name']}: {indicator['signal']} (قيمة: {indicator['value']})"
                for indicator in technical_indicators
            ])

        prompt = f"""
تحليل إشارة التداول التالية:

الأصل المالي: {asset}
التوصية المقترحة: {recommendation}
نسبة الثقة الفنية: {technical_confidence:.2f}%

نتائج التحليل الفني:

نماذج الشموع المكتشفة:
{patterns_text if patterns_text else "لا توجد نماذج مكتشفة"}

المؤشرات الفنية:
{indicators_text if indicators_text else "لا توجد مؤشرات"}

المطلوب:
1. هل توافق على هذه التوصية؟ (نعم/لا)
2. ما هي نسبة ثقتك في هذا التحليل؟ (0-100%)
3. ما هو السبب وراء تقييمك؟

يرجى الإجابة بتنسيق JSON كالتالي:
{{
    "approval": true/false,
    "confidence": رقم من 0 إلى 100,
    "reasoning": "شرح مختصر للسبب"
}}
"""
        return prompt

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """تحليل استجابة الذكاء الاصطناعي"""
        try:
            import json
            import re

            # محاولة تحليل JSON مباشرة
            if response_text.strip().startswith('{'):
                return json.loads(response_text.strip())

            # البحث عن JSON داخل النص
            json_match = re.search(r'\{[^}]+\}', response_text)
            if json_match:
                return json.loads(json_match.group())

            # تحليل نصي بديل في حال فشل JSON
            approval = any(word in response_text.lower() for word in ['نعم', 'yes', 'موافق', 'agree'])
            confidence_match = re.search(r'(\d+)%?', response_text)
            confidence = float(confidence_match.group(1)) if confidence_match else 50.0

            return {
                "approval": approval,
                "confidence": min(100, max(0, confidence)),
                "reasoning": response_text[:200] + "..." if len(response_text) > 200 else response_text
            }

        except Exception as e:
            return {
                "approval": False,
                "confidence": 0.0,
                "reasoning": f"خطأ في تحليل الاستجابة: {str(e)}"
            }
