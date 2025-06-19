import asyncio
import json
from typing import Dict, Any
import httpx
from src.ai_layer.base import BaseAIHandler
from src.models.schemas import AIResponse

class DeepSeekHandler(BaseAIHandler):
    """معالج DeepSeek API الحقيقي"""

    def __init__(self, api_key: str = None):
        super().__init__("deepseek")
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # غيّر هذا إذا كان URL مختلف

    async def analyze_signal(self, signal_data: Dict[str, Any]) -> AIResponse:
        """تحليل الإشارة باستخدام DeepSeek"""
        try:
            prompt = self.create_prompt(signal_data)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",  # استخدم اسم النموذج الصحيح من DeepSeek
                "messages": [
                    {"role": "system", "content": "أنت خبير مالي تحلل إشارات التداول."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4
            }

            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                response_text = result["choices"][0]["message"]["content"]
                parsed = self.parse_response(response_text)

                return AIResponse(
                    provider="deepseek",
                    approval=parsed["approval"],
                    confidence=parsed["confidence"],
                    reasoning=parsed["reasoning"]
                )
            else:
                return AIResponse(
                    provider="deepseek",
                    approval=False,
                    confidence=0.0,
                    reasoning=f"فشل الاتصال بـ DeepSeek: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return AIResponse(
                provider="deepseek",
                approval=False,
                confidence=0.0,
                reasoning=f"استثناء أثناء تحليل الإشارة: {str(e)}"
            )
