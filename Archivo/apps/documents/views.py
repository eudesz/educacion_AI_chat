"""
Views para gestión de documentos con información de estructura
"""

import os
import json
import logging
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import mimetypes

from .models import Document

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def document_list(request):
    """Lista todos los documentos con información de estructura"""
    try:
        # Por ahora, listar archivos del directorio estático
        # En el futuro, esto debería usar la base de datos
        documents_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')
        
        if not os.path.exists(documents_dir):
            return JsonResponse([], safe=False)
        
        documents = []
        
        # Obtener documentos de la base de datos si existen
        db_documents = Document.objects.all()
        db_docs_by_name = {doc.title: doc for doc in db_documents}
        
        for filename in os.listdir(documents_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(documents_dir, filename)
                
                # Información básica del archivo
                doc_info = {
                    'name': filename,
                    'url': f'http://localhost:8000/api/documents/serve/{filename}',
                    'id': None,
                    'structure_analyzed': False,
                    'chunks_created': False,
                    'total_chunks': 0,
                    'summary': None
                }
                
                # Si existe en la base de datos, agregar información de estructura
                if filename in db_docs_by_name:
                    db_doc = db_docs_by_name[filename]
                    doc_info.update({
                        'id': str(db_doc.id),
                        'structure_analyzed': db_doc.structure_analyzed,
                        'chunks_created': db_doc.chunks_created,
                        'total_chunks': db_doc.total_chunks,
                        'summary': db_doc.get_structure_summary()
                    })
                
                documents.append(doc_info)
        
        return JsonResponse(documents, safe=False)
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def serve_document(request, document_id):
    """Sirve un documento por ID o nombre"""
    try:
        # Intentar buscar por ID primero
        try:
            document = get_object_or_404(Document, id=document_id)
            file_path = document.file_path
        except (ValueError, Http404):
            # Si no es un UUID válido, tratar como nombre de archivo
            documents_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')
            file_path = os.path.join(documents_dir, document_id)
            
            if not os.path.exists(file_path):
                raise Http404("Document not found")
        
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        # Determinar el tipo de contenido
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'
        
        # Leer y servir el archivo
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            return response
            
    except Exception as e:
        logger.error(f"Error serving document {document_id}: {str(e)}")
        raise Http404("Document not found")

@csrf_exempt
@require_http_methods(["POST"])
def upload_document(request):
    """Sube un nuevo documento y analiza su estructura"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Validar tipo de archivo
        if not uploaded_file.name.endswith('.pdf'):
            return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)
        
        # Guardar archivo
        file_path = default_storage.save(
            f'documents/{uploaded_file.name}',
            ContentFile(uploaded_file.read())
        )
        
        # Crear registro en base de datos
        document = Document.objects.create(
            user=request.user if request.user.is_authenticated else None,
            title=uploaded_file.name,
            file_path=default_storage.path(file_path),
            file_size=uploaded_file.size,
            content_type=uploaded_file.content_type or 'application/pdf'
        )
        
        # Analizar estructura automáticamente
        from .api.structure_views import DocumentStructureView
        structure_view = DocumentStructureView()
        structure_view._analyze_document_structure(document)
        
        return JsonResponse({
            'message': 'Document uploaded successfully',
            'document_id': str(document.id),
            'structure_analyzed': document.structure_analyzed,
            'summary': document.get_structure_summary()
        })
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def download_document(request, document_id):
    """Descarga un documento"""
    try:
        document = get_object_or_404(Document, id=document_id)
        
        if not os.path.exists(document.file_path):
            raise Http404("File not found")
        
        with open(document.file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=document.content_type)
            response['Content-Disposition'] = f'attachment; filename="{document.title}"'
            return response
            
    except Exception as e:
        logger.error(f"Error downloading document {document_id}: {str(e)}")
        raise Http404("Document not found")

@csrf_exempt
@require_http_methods(["POST"])
def extract_text(request):
    """Extrae texto de un documento para el contexto"""
    try:
        data = json.loads(request.body)
        filename = data.get('filename')
        
        if not filename:
            return JsonResponse({'error': 'Filename is required'}, status=400)
        
        # Buscar el archivo
        documents_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')
        file_path = os.path.join(documents_dir, filename)
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'File not found'}, status=404)
        
        # Extraer texto usando el analizador
        from .services.structure_analyzer import DocumentStructureAnalyzer
        analyzer = DocumentStructureAnalyzer()
        
        try:
            pages_text = analyzer._extract_text_from_pdf(file_path)
            # Combinar todas las páginas
            full_text = '\n\n'.join(pages_text)
            
            # Limitar el texto para evitar contextos muy largos
            if len(full_text) > 5000:
                full_text = full_text[:5000] + "\n\n[Texto truncado - documento completo disponible]"
            
            return JsonResponse({
                'text': full_text,
                'pages': len(pages_text),
                'characters': len(full_text)
            })
            
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {str(e)}")
            return JsonResponse({'error': 'Could not extract text from PDF'}, status=500)
        
    except Exception as e:
        logger.error(f"Error in extract_text: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500) 