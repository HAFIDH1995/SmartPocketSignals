import os
from typing import Dict, Any

class ConfigManager:
    """مدير التكوين للمنصة"""
    
    def __init__(self):
        self.config = self.get_default_config()
    
    def load_config(self) -> Dict[str, Any]:
        """تحميل ملف التكوين (دائمًا يعود إلى الافتراضي في بيئة الإنتاج)"""
        return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """إرجاع التكوين الافتراضي"""
        return {
            "ai_providers": {
                "openai": {"api_key": os.environ.get("OPENAI_API_KEY", ""), "enabled": False, "weight": 0.25},
                "deepseek": {"api_key": os.environ.get("DEEPSEEK_API_KEY", ""), "enabled": False, "weight": 0.20},
                "groq": {"api_key": os.environ.get("GROQ_API_KEY", ""), "enabled": False, "weight": 0.20},
                "manus": {"api_key": os.environ.get("MANUS_API_KEY", ""), "enabled": False, "weight": 0.20},
                "grok": {"api_key": os.environ.get("GROK_API_KEY", ""), "enabled": False, "weight": 0.15}
            },
            "confidence_calculation": {
                "technical_weight": 0.6,
                "ai_weight": 0.4,
                "min_ai_approvals": 2,
                "min_final_confidence": 70
            }
        }
    
    def get_ai_config(self, provider: str) -> Dict[str, Any]:
        """الحصول على تكوين مزود ذكاء اصطناعي محدد"""
        return self.config.get("ai_providers", {}).get(provider, {})
    
    def get_confidence_config(self) -> Dict[str, Any]:
        """الحصول على تكوين حساب الثقة"""
        return self.config.get("confidence_calculation", {})
    
    def is_provider_enabled(self, provider: str) -> bool:
        """فحص ما إذا كان مزود الذكاء الاصطناعي مفعل"""
        provider_config = self.get_ai_config(provider)
        return (provider_config.get("enabled", False) and 
                bool(provider_config.get("api_key", "").strip()))
    
    def get_enabled_providers(self) -> Dict[str, Dict[str, Any]]:
        """الحصول على جميع المزودين المفعلين"""
        enabled = {}
        for provider, config in self.config.get("ai_providers", {}).items():
            if self.is_provider_enabled(provider):
                enabled[provider] = config
        return enabled
    
    # تم إزالة update_api_key و save_config لأن مفاتيح API يجب أن تدار كمتغيرات بيئة في الإنتاج

# إنشاء مثيل عام لمدير التكوين
config_manager = ConfigManager()


