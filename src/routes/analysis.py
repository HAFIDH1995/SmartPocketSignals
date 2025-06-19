import time
from datetime import datetime
from typing import List, Dict, Any
from flask import Blueprint, request, jsonify
from src.api.pocket_option import pocket_option_api
from src.analyzers.candle_patterns import CandlePatternAnalyzer
from src.analyzers.indicator_calculator import TechnicalIndicatorCalculator
from src.analyzers.trading_strategy import TradingStrategy
from src.ai_layer.chatgpt_handler import ChatGPTHandler
from src.ai_layer.deepseek import DeepSeekHandler
from src.ai_layer.groq_handler import GroqHandler
from src.ai_layer.manus_handler import ManusHandler
from src.ai_layer.grok_handler import GrokHandler
from src.models.schemas import TradingSignal, AIResponse

# إنشاء Blueprint للتحليل
analysis_bp = Blueprint('analysis', __name__)

# إنشاء مثيلات المحللات
candle_analyzer = CandlePatternAnalyzer()
indicator_calculator = TechnicalIndicatorCalculator()
trading_strategy = TradingStrategy()

# إنشاء مثيلات معالجات الذكاء الاصطناعي
ai_handlers = {
    'chatgpt': ChatGPTHandler(),
    'deepseek': DeepSeekHandler(),
    'groq': GroqHandler(),
    'manus': ManusHandler(),
    'grok': GrokHandler()
}

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_signal():
    """نقطة نهاية التحليل الرئيسية"""
    try:
        # الحصول على البيانات من الطلب
        data = request.get_json() or {}
        asset = data.get('asset', 'EURUSD_OTC')
        
        # محاكاة الاتصال بـ Pocket Option
        time.sleep(0.1)  # محاكاة تأخير الاتصال
        
        # تحليل عينة من الأطر الزمنية (للاختبار)
        test_timeframes = ['1m', '5m', '15m', '30m', '1h']
        timeframe_analyses = []
        
        for timeframe in test_timeframes:
            try:
                # محاكاة جلب بيانات الشموع
                from src.models.schemas import CandleData
                import random
                from datetime import timedelta
                
                # توليد بيانات تجريبية
                candles = []
                base_price = 1.1000
                current_time = datetime.now()
                
                for i in range(50):
                    timestamp = current_time - timedelta(minutes=i)
                    price_change = random.uniform(-0.002, 0.002)
                    open_price = base_price + price_change
                    close_price = open_price + random.uniform(-0.001, 0.001)
                    high_price = max(open_price, close_price) + random.uniform(0, 0.0005)
                    low_price = min(open_price, close_price) - random.uniform(0, 0.0005)
                    
                    candle = CandleData(
                        timestamp=timestamp,
                        open=round(open_price, 5),
                        high=round(high_price, 5),
                        low=round(low_price, 5),
                        close=round(close_price, 5),
                        volume=random.uniform(1000, 5000)
                    )
                    candles.append(candle)
                
                # تحليل نماذج الشموع
                candle_patterns = candle_analyzer.analyze_patterns(candles)
                
                # حساب المؤشرات الفنية
                technical_indicators = indicator_calculator.calculate_all_indicators(candles)
                
                # تحليل الإطار الزمني
                timeframe_analysis = trading_strategy.analyze_timeframe(
                    timeframe, candle_patterns, technical_indicators
                )
                
                timeframe_analyses.append(timeframe_analysis)
                
            except Exception as e:
                print(f"خطأ في تحليل الإطار الزمني {timeframe}: {str(e)}")
                continue
        
        if not timeframe_analyses:
            return jsonify({
                'success': False,
                'message': 'فشل في جلب البيانات أو التحليل',
                'error': 'لا توجد بيانات كافية للتحليل'
            }), 400
        
        # توليد الإشارة الفنية
        recommendation, technical_confidence, trade_details = trading_strategy.generate_signal(
            timeframe_analyses, asset
        )
        
        # إعداد بيانات للذكاء الاصطناعي
        ai_signal_data = {
            'asset': asset,
            'recommendation': recommendation,
            'technical_confidence': technical_confidence,
            'candle_patterns': [
                {
                    'name': pattern.name,
                    'detected': pattern.detected,
                    'signal': pattern.signal,
                    'confidence': pattern.confidence
                }
                for analysis in timeframe_analyses
                for pattern in analysis.candle_patterns
                if pattern.detected
            ],
            'technical_indicators': [
                {
                    'name': indicator.name,
                    'signal': indicator.signal,
                    'value': indicator.value
                }
                for analysis in timeframe_analyses
                for indicator in analysis.technical_indicators
            ],
            'timeframe_analyses': [
                {
                    'timeframe': analysis.timeframe,
                    'signal': analysis.overall_signal,
                    'score': analysis.score
                }
                for analysis in timeframe_analyses
            ]
        }
        
        # محاكاة التحقق عبر الذكاء الاصطناعي (متزامن)
        ai_responses = []
        
        for handler_name, handler in ai_handlers.items():
            try:
                # محاكاة استجابة الذكاء الاصطناعي
                time.sleep(0.1)  # محاكاة تأخير
                
                if recommendation == 'hold':
                    approval = False
                    confidence = 20.0
                elif technical_confidence >= 85:
                    approval = True
                    confidence = min(90.0, technical_confidence)
                else:
                    approval = False
                    confidence = 40.0
                
                ai_response = AIResponse(
                    provider=handler_name,
                    approval=approval,
                    confidence=confidence,
                    reasoning=f"تحليل محاكي من {handler_name}"
                )
                ai_responses.append(ai_response)
                
            except Exception as e:
                print(f"خطأ في معالج الذكاء الاصطناعي {handler_name}: {str(e)}")
                continue
        
        # حساب نسبة الثقة النهائية
        ai_confidence = calculate_ai_confidence(ai_responses)
        final_confidence = calculate_final_confidence(technical_confidence, ai_confidence)
        
        # إنشاء الإشارة النهائية
        trading_signal = TradingSignal(
            asset=asset,
            recommendation=recommendation,
            entry_time=trade_details.get('entry_time'),
            trade_duration=trade_details.get('duration'),
            target_price=trade_details.get('target_price'),
            technical_confidence=technical_confidence,
            ai_confidence=ai_confidence,
            final_confidence=final_confidence,
            timeframe_analyses=timeframe_analyses,
            ai_responses=ai_responses,
            created_at=datetime.now()
        )
        
        # إرجاع النتيجة
        return jsonify({
            'success': True,
            'message': 'تم التحليل بنجاح',
            'signal': {
                'asset': trading_signal.asset,
                'recommendation': trading_signal.recommendation,
                'entry_time': trading_signal.entry_time.isoformat() if trading_signal.entry_time else None,
                'trade_duration': trading_signal.trade_duration,
                'target_price': trading_signal.target_price,
                'technical_confidence': round(trading_signal.technical_confidence, 2),
                'ai_confidence': round(trading_signal.ai_confidence, 2),
                'final_confidence': round(trading_signal.final_confidence, 2),
                'ai_responses': [
                    {
                        'provider': response.provider,
                        'approval': response.approval,
                        'confidence': response.confidence,
                        'reasoning': response.reasoning
                    }
                    for response in trading_signal.ai_responses
                ],
                'created_at': trading_signal.created_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء التحليل',
            'error': str(e)
        }), 500

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """فحص حالة النظام"""
    return jsonify({
        'status': 'healthy',
        'message': 'النظام يعمل بشكل طبيعي',
        'timestamp': datetime.now().isoformat(),
        'ai_providers': list(ai_handlers.keys())
    })

def calculate_ai_confidence(ai_responses: List[AIResponse]) -> float:
    """حساب متوسط ثقة الذكاء الاصطناعي"""
    if not ai_responses:
        return 0.0
    
    # حساب متوسط الثقة للاستجابات المؤيدة فقط
    approving_responses = [r for r in ai_responses if r.approval]
    
    if not approving_responses:
        return 0.0
    
    total_confidence = sum(r.confidence for r in approving_responses)
    return total_confidence / len(approving_responses)

def calculate_final_confidence(technical_confidence: float, ai_confidence: float) -> float:
    """حساب نسبة الثقة النهائية"""
    # وزن التحليل الفني: 60%
    # وزن الذكاء الاصطناعي: 40%
    technical_weight = 0.6
    ai_weight = 0.4
    
    final_confidence = (
        (technical_confidence * technical_weight) + 
        (ai_confidence * ai_weight)
    )
    
    return round(final_confidence, 2)

