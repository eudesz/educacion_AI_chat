from django.urls import path
from . import views
from .views import DocumentListView, ServeDocumentView, ExtractTextAPIView

# Importar las vistas de estructura desde apps.documents
from apps.documents.api.structure_views import DocumentStructureView, ContextManagementView, get_document_chunks

urlpatterns = [
    # URLs básicas para documents
    path('list/', DocumentListView.as_view(), name='document-list'),
    path('serve/<str:filename>/', ServeDocumentView.as_view(), name='document-serve'),
    path('extract_text/', ExtractTextAPIView.as_view(), name='document-extract-text'),
    
    # Nuevos endpoints de estructura
    path('api/list/', views.document_list, name='document-api-list'),
    path('api/structure/<uuid:document_id>/', views.document_structure, name='document-structure'),
    path('api/chunks/<uuid:document_id>/', views.document_chunks, name='document-chunks'),
    path('api/analyze-all/', views.analyze_all_documents, name='analyze-all-documents'),
    
    # APIs avanzadas para estructura y contexto
    path('api/structure/<uuid:document_id>/', DocumentStructureView.as_view(), name='document_structure_advanced'),
    path('api/chunks/<uuid:document_id>/', get_document_chunks, name='document_chunks_advanced'),
    path('api/context/', ContextManagementView.as_view(), name='context_management'),
]
