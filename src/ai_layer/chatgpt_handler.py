import asyncio
import json
from typing import Dict, Any
import httpx
from src.ai_layer.base import BaseAIHandler
from src.models.schemas import AIResponse

class ChatGPTHandler(BaseAIHandler):
    """معالج ChatGPT"""

    def __init__(self, api_key: str = None):
        super().__init__("chatgpt")
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def analyze_signal(self, signal_data: Dict[str, Any]) -> AIResponse:
        """تحليل الإشارة باستخدام OpenAI ChatGPT API"""

        try:
            prompt = self.create_prompt(signal_data)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "gpt-4",  # أو gpt-3.5-turbo إذا أردت نسخة أسرع وأرخص
                "messages": [
                    {"role": "system", "content": "أنت خبير تحليل فني في سوق الفوركس والخيارات الثنائية. عند تقديم إشارة، قرر إن كانت مناسبة للتداول، ما نسبة الثقة بها، ولماذا."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }

            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                parsed = self.parse_response(content)

                return AIResponse(
                    provider="chatgpt",
                    approval=parsed["approval"],
                    confidence=parsed["confidence"],
                    reasoning=parsed["reasoning"]
                )
            else:
                return AIResponse(
                    provider="chatgpt",
                    approval=False,
                    confidence=0.0,
                    reasoning=f"فشل الاتصال بـ OpenAI: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return AIResponse(
                provider="chatgpt",
                approval=False,
                confidence=0.0,
                reasoning=f"استثناء أثناء تحليل ChatGPT: {str(e)}"
            )
