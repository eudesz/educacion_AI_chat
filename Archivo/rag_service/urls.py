from django.urls import path
from rag import views

urlpatterns = [
    # Endpoint de prueba para categorización
    path('test-categorization/', views.test_medical_categorization, name='test_categorization'),

    # Endpoint para verificar sistema de embeddings
    path('embedding-status/', views.embedding_service_status, name='embedding_status'),
    
    # NUEVOS ENDPOINTS DE INVESTIGACIÓN
    path('confidence-stats/', views.confidence_stats, name='confidence_stats'),
    path('pattern-detection-test/', views.pattern_detection_test, name='pattern_detection_test'),
    path('system-improvements/', views.system_improvements, name='system_improvements'),
] 