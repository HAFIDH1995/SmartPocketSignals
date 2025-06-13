// SmartPocketSignals - JavaScript

class SmartPocketSignals {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentAnalysis = null;
        this.isAnalyzing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkSystemHealth();
    }

    initializeElements() {
        // Sections
        this.analysisSection = document.getElementById('analysisSection');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');

        // Controls
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.assetSelect = document.getElementById('assetSelect');
        this.newAnalysisBtn = document.getElementById('newAnalysisBtn');
        this.retryBtn = document.getElementById('retryBtn');
        this.shareBtn = document.getElementById('shareBtn');

        // Status
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');

        // Loading
        this.loadingText = document.getElementById('loadingText');
        this.progressFill = document.getElementById('progressFill');

        // Results
        this.timestamp = document.getElementById('timestamp');
        this.recommendationCard = document.getElementById('recommendationCard');
        this.recommendationIcon = document.getElementById('recommendationIcon');
        this.recommendationTitle = document.getElementById('recommendationTitle');
        this.recommendationAsset = document.getElementById('recommendationAsset');
        this.confidenceBadge = document.getElementById('confidenceBadge');
        this.confidenceValue = document.getElementById('confidenceValue');
        this.entryTime = document.getElementById('entryTime');
        this.tradeDuration = document.getElementById('tradeDuration');
        this.targetPrice = document.getElementById('targetPrice');
        this.technicalConfidence = document.getElementById('technicalConfidence');
        this.aiConfidence = document.getElementById('aiConfidence');
        this.technicalConfidenceBar = document.getElementById('technicalConfidenceBar');
        this.aiConfidenceBar = document.getElementById('aiConfidenceBar');
        this.aiGrid = document.getElementById('aiGrid');

        // Error
        this.errorMessage = document.getElementById('errorMessage');
    }

    bindEvents() {
        this.analyzeBtn.addEventListener('click', () => this.startAnalysis());
        this.newAnalysisBtn.addEventListener('click', () => this.resetToAnalysis());
        this.retryBtn.addEventListener('click', () => this.startAnalysis());
        this.shareBtn.addEventListener('click', () => this.shareResults());
    }

    async checkSystemHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateStatus('متصل', 'success');
            } else {
                this.updateStatus('غير متصل', 'error');
            }
        } catch (error) {
            console.error('خطأ في فحص حالة النظام:', error);
            this.updateStatus('خطأ في الاتصال', 'error');
        }
    }

    updateStatus(text, type) {
        this.statusText.textContent = text;
        this.statusDot.className = `status-dot ${type}`;
    }

    async startAnalysis() {
        if (this.isAnalyzing) return;

        this.isAnalyzing = true;
        this.analyzeBtn.disabled = true;
        
        const selectedAsset = this.assetSelect.value;
        
        // إخفاء جميع الأقسام وإظهار قسم التحميل
        this.hideAllSections();
        this.showSection(this.loadingSection);
        
        // بدء رسائل التحميل
        this.startLoadingMessages();

        try {
            const response = await fetch(`${this.apiBaseUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    asset: selectedAsset
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentAnalysis = data.signal;
                this.displayResults();
            } else {
                this.showError(data.message || 'فشل في التحليل');
            }
        } catch (error) {
            console.error('خطأ في التحليل:', error);
            this.showError('خطأ في الاتصال بالخادم');
        } finally {
            this.isAnalyzing = false;
            this.analyzeBtn.disabled = false;
        }
    }

    startLoadingMessages() {
        const messages = [
            'جاري الاتصال بـ Pocket Option...',
            'تحليل الأطر الزمنية المختلفة...',
            'حساب المؤشرات الفنية...',
            'تحليل نماذج الشموع...',
            'التحقق عبر الذكاء الاصطناعي...',
            'حساب نسبة الثقة النهائية...',
            'إعداد النتائج...'
        ];

        let currentIndex = 0;
        const interval = setInterval(() => {
            if (currentIndex < messages.length && this.isAnalyzing) {
                this.loadingText.textContent = messages[currentIndex];
                currentIndex++;
            } else {
                clearInterval(interval);
            }
        }, 800);
    }

    displayResults() {
        this.hideAllSections();
        this.showSection(this.resultsSection);

        const signal = this.currentAnalysis;
        
        // تحديث الطابع الزمني
        this.timestamp.textContent = new Date(signal.created_at).toLocaleString('ar-SA');

        // تحديث التوصية الرئيسية
        this.updateRecommendation(signal);

        // تحديث تفاصيل الصفقة
        this.updateTradeDetails(signal);

        // تحديث نسب الثقة
        this.updateConfidenceBreakdown(signal);

        // تحديث استجابات الذكاء الاصطناعي
        this.updateAIResponses(signal.ai_responses);

        // إضافة تأثيرات الحركة
        this.resultsSection.classList.add('fade-in');
    }

    updateRecommendation(signal) {
        const recommendationMap = {
            'buy': {
                title: 'توصية الشراء',
                icon: '📈',
                class: 'buy'
            },
            'sell': {
                title: 'توصية البيع',
                icon: '📉',
                class: 'sell'
            },
            'hold': {
                title: 'لا توجد توصية',
                icon: '⏸️',
                class: 'hold'
            }
        };

        const rec = recommendationMap[signal.recommendation] || recommendationMap['hold'];
        
        this.recommendationTitle.textContent = rec.title;
        this.recommendationIcon.textContent = rec.icon;
        this.recommendationAsset.textContent = signal.asset;
        this.confidenceValue.textContent = `${signal.final_confidence}%`;
        
        // تحديث لون بطاقة التوصية
        this.recommendationCard.className = `recommendation-card ${rec.class}`;
        
        // تحديث لون شارة الثقة
        const confidenceColor = this.getConfidenceColor(signal.final_confidence);
        this.confidenceValue.style.color = confidenceColor;
    }

    updateTradeDetails(signal) {
        this.entryTime.textContent = signal.entry_time ? 
            new Date(signal.entry_time).toLocaleTimeString('ar-SA') : '--';
        this.tradeDuration.textContent = signal.trade_duration || '--';
        this.targetPrice.textContent = signal.target_price ? 
            signal.target_price.toFixed(5) : '--';
    }

    updateConfidenceBreakdown(signal) {
        // التحليل الفني
        this.technicalConfidence.textContent = `${signal.technical_confidence}%`;
        this.technicalConfidenceBar.style.width = `${signal.technical_confidence}%`;
        this.technicalConfidenceBar.style.backgroundColor = this.getConfidenceColor(signal.technical_confidence);

        // الذكاء الاصطناعي
        this.aiConfidence.textContent = `${signal.ai_confidence}%`;
        this.aiConfidenceBar.style.width = `${signal.ai_confidence}%`;
        this.aiConfidenceBar.style.backgroundColor = this.getConfidenceColor(signal.ai_confidence);
    }

    updateAIResponses(aiResponses) {
        this.aiGrid.innerHTML = '';

        aiResponses.forEach(response => {
            const card = document.createElement('div');
            card.className = `ai-response-card ${response.approval ? 'approved' : 'rejected'}`;
            
            card.innerHTML = `
                <div class="ai-provider">${response.provider}</div>
                <div class="ai-status">${response.approval ? '✅ موافق' : '❌ مرفوض'}</div>
                <div class="ai-confidence">${response.confidence}%</div>
                <div class="ai-reasoning" title="${response.reasoning}">
                    ${response.reasoning.length > 50 ? 
                        response.reasoning.substring(0, 50) + '...' : 
                        response.reasoning}
                </div>
            `;
            
            this.aiGrid.appendChild(card);
        });
    }

    getConfidenceColor(confidence) {
        if (confidence >= 80) return '#4CAF50';
        if (confidence >= 60) return '#FF9800';
        return '#f44336';
    }

    showError(message) {
        this.hideAllSections();
        this.showSection(this.errorSection);
        this.errorMessage.textContent = message;
    }

    hideAllSections() {
        [this.analysisSection, this.loadingSection, this.resultsSection, this.errorSection]
            .forEach(section => section.classList.add('hidden'));
    }

    showSection(section) {
        section.classList.remove('hidden');
        section.classList.add('slide-up');
    }

    resetToAnalysis() {
        this.hideAllSections();
        this.showSection(this.analysisSection);
        this.currentAnalysis = null;
        
        // إعادة تعيين الأزرار
        this.analyzeBtn.disabled = false;
        this.isAnalyzing = false;
    }

    shareResults() {
        if (!this.currentAnalysis) return;

        const signal = this.currentAnalysis;
        const shareText = `
🔔 إشارة SmartPocketSignals

📊 الأصل: ${signal.asset}
${signal.recommendation === 'buy' ? '📈' : signal.recommendation === 'sell' ? '📉' : '⏸️'} التوصية: ${this.getRecommendationText(signal.recommendation)}
🎯 نسبة الثقة: ${signal.final_confidence}%
⏰ وقت الدخول: ${signal.entry_time ? new Date(signal.entry_time).toLocaleTimeString('ar-SA') : '--'}
⏱️ مدة الصفقة: ${signal.trade_duration || '--'}

💡 مدعوم بالتحليل الفني والذكاء الاصطناعي
        `.trim();

        if (navigator.share) {
            navigator.share({
                title: 'إشارة SmartPocketSignals',
                text: shareText
            });
        } else {
            // نسخ إلى الحافظة
            navigator.clipboard.writeText(shareText).then(() => {
                this.showNotification('تم نسخ النتائج إلى الحافظة');
            });
        }
    }

    getRecommendationText(recommendation) {
        const map = {
            'buy': 'شراء',
            'sell': 'بيع',
            'hold': 'انتظار'
        };
        return map[recommendation] || 'غير محدد';
    }

    showNotification(message) {
        // إنشاء إشعار بسيط
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// تشغيل التطبيق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new SmartPocketSignals();
});

// إضافة أنماط CSS للإشعارات
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification {
        font-family: 'Cairo', sans-serif;
        font-weight: 500;
    }
`;
document.head.appendChild(style);

