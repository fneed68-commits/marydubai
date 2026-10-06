# MaryDubai Multi-Agent System

نظام وكلاء متعدد للاستخدامات الأمنية والمالية والقانونية،
مع تحكم بشري صارم (HITL) ودعم RAG للبحث الذكي.

## المكونات

### الوكلاء
- financial_investment_agent.py — وكيل الاستثمار المالي
- legal_consultant_agent.py — المستشار القانوني
- loop_breaker_agent.py — كسر الحلقات اللانهائية
- math_physics_agent.py — الرياضيات والفيزياء
- temporal_edge_agent.py — الحواف الزمنية
- wallet_security_agent.py — أمن المحافظ
- rag_time_manager_agent.py — RAG للبحث الذكي

### البنية التحتية
- shared/embeddings.py — Embedders
- shared/vector_store.py — SQLite Vector Store
- index_builder.py — سكربت بناء الـ Index

## الاستخدام

### اختبار سريع
python3 rag_time_manager_agent.py

### بناء Index
python3 index_builder.py --source ./ --local

## النمط الأمني (HITL)
كل وكيل يتوقف عند نقطة قرار وينتظر أمر "yes" صريحاً.
