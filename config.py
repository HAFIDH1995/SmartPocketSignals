import json
import os
from typing import Dict, Any

class ConfigManager:
    """مدير التكوين للمنصة"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """تحميل ملف التكوين"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ملف التكوين غير موجود: {self.config_path}")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            print(f"خطأ في تحليل ملف التكوين: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """إرجاع التكوين الافتراضي"""
        return {
            "ai_providers": {
                "openai": {"api_key": "", "enabled": False, "weight": 0.25},
                "deepseek": {"api_key": "", "enabled": False, "weight": 0.20},
                "groq": {"api_key": "", "enabled": False, "weight": 0.20},
                "manus": {"api_key": "", "enabled": False, "weight": 0.20},
                "grok": {"api_key": "", "enabled": False, "weight": 0.15}
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
        return self.config.get('ai_providers', {}).get(provider, {})
    
    def get_confidence_config(self) -> Dict[str, Any]:
        """الحصول على تكوين حساب الثقة"""
        return self.config.get('confidence_calculation', {})
    
    def is_provider_enabled(self, provider: str) -> bool:
        """فحص ما إذا كان مزود الذكاء الاصطناعي مفعل"""
        provider_config = self.get_ai_config(provider)
        return (provider_config.get('enabled', False) and 
                bool(provider_config.get('api_key', '').strip()))
    
    def get_enabled_providers(self) -> Dict[str, Dict[str, Any]]:
        """الحصول على جميع المزودين المفعلين"""
        enabled = {}
        for provider, config in self.config.get('ai_providers', {}).items():
            if self.is_provider_enabled(provider):
                enabled[provider] = config
        return enabled
    
    def update_api_key(self, provider: str, api_key: str):
        """تحديث مفتاح API لمزود محدد"""
        if provider in self.config.get('ai_providers', {}):
            self.config['ai_providers'][provider]['api_key'] = api_key
            self.config['ai_providers'][provider]['enabled'] = bool(api_key.strip())
            self.save_config()
    
    def save_config(self):
        """حفظ التكوين إلى الملف"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ ملف التكوين: {e}")

# إنشاء مثيل عام لمدير التكوين
config_manager = ConfigManager()

