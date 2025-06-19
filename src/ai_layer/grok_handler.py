import asyncio
import json
from typing import Dict, Any
import httpx
from src.ai_layer.base import BaseAIHandler
from src.models.schemas import AIResponse

class GrokHandler(BaseAIHandler):
    """معالج Grok API الحقيقي"""
    
    def __init__(self, api_key: str = None):
        super().__init__("grok")
        self.api_key = api_key
        self.api_url = "https://api.grok.com/v1/chat/completions"  # غيّره إذا كان مختلفًا

    async def analyze_signal(self, signal_data: Dict[str, Any]) -> AIResponse:
        """تحليل الإشارة باستخدام Grok API"""
        try:
            prompt = self.create_prompt(signal_data)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "grok-trading-expert",  # غيّره إن كان هناك اسم نموذج معين
                "messages": [
                    {"role": "system", "content": "أنت مساعد خبير في التداول الفني. قم بتحليل الإشارة بناءً على المؤشرات والأطر الزمنية وأعط قراراً نهائياً."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }

            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                response_text = result["choices"][0]["message"]["content"]
                parsed = self.parse_response(response_text)

                return AIResponse(
                    provider="grok",
                    approval=parsed["approval"],
                    confidence=parsed["confidence"],
                    reasoning=parsed["reasoning"]
                )
            else:
                return AIResponse(
                    provider="grok",
                    approval=False,
                    confidence=0.0,
                    reasoning=f"فشل الاتصال بـ Grok: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return AIResponse(
                provider="grok",
                approval=False,
                confidence=0.0,
                reasoning=f"استثناء أثناء تحليل الإشارة: {str(e)}"
            )
