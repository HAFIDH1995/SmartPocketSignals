import asyncio
import json
from typing import Dict, Any
import httpx
from src.ai_layer.base import BaseAIHandler
from src.models.schemas import AIResponse

class GroqHandler(BaseAIHandler):
    """معالج Groq API الحقيقي"""
    
    def __init__(self, api_key: str = None):
        super().__init__("groq")
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"  # تأكد أن هذا هو العنوان الصحيح

    async def analyze_signal(self, signal_data: Dict[str, Any]) -> AIResponse:
        """تحليل الإشارة باستخدام Groq API"""
        try:
            prompt = self.create_prompt(signal_data)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mixtral-8x7b-32768",  # غيّره إن كنت تستخدم نموذج مختلف
                "messages": [
                    {"role": "system", "content": "أنت خبير تحلل إشارات التداول وتحكم على التوصية بناءً على التحليل الفني."},
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
                    provider="groq",
                    approval=parsed["approval"],
                    confidence=parsed["confidence"],
                    reasoning=parsed["reasoning"]
                )
            else:
                return AIResponse(
                    provider="groq",
                    approval=False,
                    confidence=0.0,
                    reasoning=f"فشل الاتصال بـ Groq: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return AIResponse(
                provider="groq",
                approval=False,
                confidence=0.0,
                reasoning=f"استثناء أثناء تحليل الإشارة: {str(e)}"
            )
