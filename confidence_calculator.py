from typing import List, Dict, Any
from src.models.signal import AIResponse
from src.utils.config import config_manager

class AIConfidenceCalculator:
    """حاسبة نسبة الثقة المحسنة للذكاء الاصطناعي"""
    
    def __init__(self):
        self.confidence_config = config_manager.get_confidence_config()
        self.technical_weight = self.confidence_config.get('technical_weight', 0.6)
        self.ai_weight = self.confidence_config.get('ai_weight', 0.4)
        self.min_ai_approvals = self.confidence_config.get('min_ai_approvals', 2)
        self.min_final_confidence = self.confidence_config.get('min_final_confidence', 70)
    
    def calculate_ai_confidence(self, ai_responses: List[AIResponse]) -> Dict[str, Any]:
        """حساب نسبة الثقة المحسنة للذكاء الاصطناعي"""
        
        if not ai_responses:
            return {
                'confidence': 0.0,
                'approvals': 0,
                'rejections': 0,
                'consensus': 'none',
                'weighted_score': 0.0
            }
        
        # تصنيف الاستجابات
        approving_responses = [r for r in ai_responses if r.approval]
        rejecting_responses = [r for r in ai_responses if not r.approval]
        
        # حساب النقاط المرجحة
        total_weighted_score = 0.0
        total_weight = 0.0
        
        enabled_providers = config_manager.get_enabled_providers()
        
        for response in ai_responses:
            provider_config = enabled_providers.get(response.provider, {})
            weight = provider_config.get('weight', 0.2)
            
            if response.approval:
                # نقاط إيجابية للموافقة
                score = (response.confidence / 100) * weight
                total_weighted_score += score
            else:
                # نقاط سلبية للرفض
                penalty = (response.confidence / 100) * weight * 0.5
                total_weighted_score -= penalty
            
            total_weight += weight
        
        # تطبيع النتيجة
        if total_weight > 0:
            normalized_score = (total_weighted_score / total_weight) * 100
            ai_confidence = max(0, min(100, normalized_score))
        else:
            ai_confidence = 0.0
        
        # تحديد الإجماع
        total_responses = len(ai_responses)
        approval_ratio = len(approving_responses) / total_responses if total_responses > 0 else 0
        
        if approval_ratio >= 0.8:
            consensus = 'strong_approval'
        elif approval_ratio >= 0.6:
            consensus = 'moderate_approval'
        elif approval_ratio >= 0.4:
            consensus = 'mixed'
        elif approval_ratio >= 0.2:
            consensus = 'moderate_rejection'
        else:
            consensus = 'strong_rejection'
        
        return {
            'confidence': round(ai_confidence, 2),
            'approvals': len(approving_responses),
            'rejections': len(rejecting_responses),
            'consensus': consensus,
            'weighted_score': round(total_weighted_score, 4),
            'approval_ratio': round(approval_ratio, 2)
        }
    
    def calculate_final_confidence(self, technical_confidence: float, 
                                 ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """حساب نسبة الثقة النهائية المحسنة"""
        
        ai_confidence = ai_analysis['confidence']
        consensus = ai_analysis['consensus']
        approvals = ai_analysis['approvals']
        
        # التحقق من الحد الأدنى للموافقات
        if approvals < self.min_ai_approvals:
            # تقليل الثقة إذا لم تكن هناك موافقات كافية
            ai_penalty = 0.3
            adjusted_ai_confidence = ai_confidence * (1 - ai_penalty)
        else:
            adjusted_ai_confidence = ai_confidence
        
        # حساب الثقة الأساسية
        base_confidence = (
            (technical_confidence * self.technical_weight) + 
            (adjusted_ai_confidence * self.ai_weight)
        )
        
        # تطبيق مكافآت وعقوبات الإجماع
        consensus_modifiers = {
            'strong_approval': 1.1,      # مكافأة 10%
            'moderate_approval': 1.05,   # مكافأة 5%
            'mixed': 0.95,               # عقوبة 5%
            'moderate_rejection': 0.85,  # عقوبة 15%
            'strong_rejection': 0.7,     # عقوبة 30%
            'none': 0.8                  # عقوبة 20%
        }
        
        modifier = consensus_modifiers.get(consensus, 1.0)
        final_confidence = base_confidence * modifier
        
        # تحديد التوصية النهائية
        if final_confidence >= self.min_final_confidence and approvals >= self.min_ai_approvals:
            recommendation_status = 'approved'
        elif final_confidence >= 50:
            recommendation_status = 'conditional'
        else:
            recommendation_status = 'rejected'
        
        return {
            'final_confidence': round(max(0, min(100, final_confidence)), 2),
            'base_confidence': round(base_confidence, 2),
            'consensus_modifier': modifier,
            'recommendation_status': recommendation_status,
            'technical_contribution': round(technical_confidence * self.technical_weight, 2),
            'ai_contribution': round(adjusted_ai_confidence * self.ai_weight, 2),
            'meets_minimum_approvals': approvals >= self.min_ai_approvals,
            'meets_minimum_confidence': final_confidence >= self.min_final_confidence
        }
    
    def get_confidence_explanation(self, technical_confidence: float, 
                                 ai_analysis: Dict[str, Any], 
                                 final_analysis: Dict[str, Any]) -> str:
        """إنشاء شرح مفصل لحساب الثقة"""
        
        explanation_parts = []
        
        # التحليل الفني
        explanation_parts.append(f"التحليل الفني: {technical_confidence}% (وزن {self.technical_weight*100}%)")
        
        # الذكاء الاصطناعي
        ai_conf = ai_analysis['confidence']
        approvals = ai_analysis['approvals']
        total_responses = approvals + ai_analysis['rejections']
        
        explanation_parts.append(f"الذكاء الاصطناعي: {ai_conf}% (وزن {self.ai_weight*100}%)")
        explanation_parts.append(f"الموافقات: {approvals}/{total_responses}")
        
        # الإجماع
        consensus_text = {
            'strong_approval': 'إجماع قوي على الموافقة',
            'moderate_approval': 'إجماع متوسط على الموافقة',
            'mixed': 'آراء متضاربة',
            'moderate_rejection': 'إجماع متوسط على الرفض',
            'strong_rejection': 'إجماع قوي على الرفض',
            'none': 'لا يوجد إجماع'
        }
        
        consensus = ai_analysis['consensus']
        explanation_parts.append(f"الإجماع: {consensus_text.get(consensus, 'غير محدد')}")
        
        # النتيجة النهائية
        final_conf = final_analysis['final_confidence']
        status = final_analysis['recommendation_status']
        
        status_text = {
            'approved': 'مقبولة',
            'conditional': 'مشروطة',
            'rejected': 'مرفوضة'
        }
        
        explanation_parts.append(f"النتيجة النهائية: {final_conf}% - {status_text.get(status, 'غير محدد')}")
        
        return " | ".join(explanation_parts)

# إنشاء مثيل عام لحاسبة الثقة
confidence_calculator = AIConfidenceCalculator()

