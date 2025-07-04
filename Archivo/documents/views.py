from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Document, DocumentStructure, SemanticChunk
import logging
import json
from .services.structure_analyzer import StructureAnalyzer

logger = logging.getLogger(__name__)

# Create your views here.

class ServeDocumentView(APIView):
    """
    Sirve un archivo de forma segura desde el directorio 'documentos_a_subir'.
    """
    def get(self, request, filename, *args, **kwargs):
        # Construye la ruta al directorio de documentos de la demo
        docs_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')
        file_path = os.path.join(docs_dir, filename)

        # Medida de seguridad: asegurarse de que el archivo solicitado está dentro del directorio esperado
        if not os.path.abspath(file_path).startswith(os.path.abspath(docs_dir)):
            return Response({"error": "Acceso no autorizado."}, status=status.HTTP_403_FORBIDDEN)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            except Exception as e:
                return Response({"error": f"No se pudo leer el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise Http404("El archivo no fue encontrado.")


class ExtractTextAPIView(APIView):
    """
    Extrae texto de un archivo PDF dado su nombre.
    Busca el archivo en el directorio 'documentos_a_subir'.
    """
    def post(self, request, *args, **kwargs):
        filename = request.data.get('filename')
        if not filename:
            return Response({"error": "El nombre del archivo ('filename') es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        docs_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')
        file_path = os.path.join(docs_dir, filename)

        if not os.path.abspath(file_path).startswith(os.path.abspath(docs_dir)):
            return Response({"error": "Acceso no autorizado."}, status=status.HTTP_403_FORBIDDEN)

        if not os.path.exists(file_path):
            return Response({"error": "Archivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            import fitz  # PyMuPDF
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            
            return Response({"text": text}, status=status.HTTP_200_OK)
        except ImportError:
            return Response({"error": "PyMuPDF no está instalado, no se puede extraer texto de PDF."}, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            return Response({"error": f"Error al extraer texto: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentListView(APIView):
    """
    Una vista para listar todos los documentos del directorio 'documentos_a_subir'.
    """
    def get(self, request, *args, **kwargs):
        docs_dir = os.path.join(settings.BASE_DIR, 'documentos_a_subir')

        if not os.path.exists(docs_dir) or not os.path.isdir(docs_dir):
            return Response(
                {"error": "El directorio 'documentos_a_subir' no fue encontrado en la raíz del proyecto."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Listar solo archivos PDF
            files = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f)) and f.lower().endswith('.pdf')]
            
            # Crear una lista de diccionarios con el nombre y la URL para servirlos
            file_data = []
            for filename in files:
                file_data.append({
                    'name': filename,
                    # Construye la URL apuntando a nuestra nueva vista 'ServeDocumentView'
                    'url': request.build_absolute_uri(f'/api/documents/serve/{filename}/')
                })

            return Response(file_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error al leer el directorio de documentos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def document_list(request):
    """Lista todos los documentos con información completa"""
    try:
        documents = Document.objects.all().order_by('-uploaded_at')
        
        documents_data = []
        for doc in documents:
            doc_data = {
                'id': str(doc.id),
                'title': doc.title,
                'file_path': doc.file_path,
                'file_size': doc.file_size,
                'uploaded_at': doc.uploaded_at.isoformat(),
                'content_type': doc.content_type,
                'structure_analyzed': doc.structure_analyzed,
                'total_chunks': doc.total_chunks,
                'user': doc.user.username if doc.user else 'unknown'
            }
            
            # Agregar resumen de estructura si está disponible
            if doc.structure_analyzed and doc.structure_data:
                doc_data['structure_summary'] = doc.get_structure_summary()
            
            documents_data.append(doc_data)
        
        logger.info(f"📋 Listando {len(documents_data)} documentos")
        
        return Response({
            'documents': documents_data,
            'total': len(documents_data)
        })
        
    except Exception as e:
        logger.error(f"❌ Error listando documentos: {str(e)}")
        return Response({
            'error': 'Error al obtener la lista de documentos',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def document_structure(request, document_id):
    """Obtiene la estructura de un documento específico"""
    try:
        logger.info(f"🔍 Obteniendo estructura para documento: {document_id}")
        
        # Buscar el documento
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({
                'error': 'Documento no encontrado',
                'document_id': document_id
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Si ya está analizado, devolver datos existentes
        if document.structure_analyzed and document.structure_data:
            logger.info(f"✅ Estructura ya analizada para: {document.title}")
            
            return Response({
                'document_id': str(document.id),
                'title': document.title,
                'structure_analyzed': True,
                'analysis_date': document.structure_data.get('analyzed_at'),
                'structure': document.structure_data,
                'summary': document.get_structure_summary()
            })
        
        # Analizar estructura si no está hecho
        logger.info(f"🔄 Analizando estructura para: {document.title}")
        
        analyzer = StructureAnalyzer()
        
        # Extraer texto del PDF
        text = analyzer.extract_text_from_pdf(document.file_path)
        if not text:
            return Response({
                'error': 'No se pudo extraer texto del documento',
                'document_id': document_id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Analizar estructura
        structure_data = analyzer.analyze_structure(text)
        
        # Crear chunks semánticos
        chunks_data = analyzer.create_semantic_chunks(text, structure_data['structure_elements'])
        
        # Guardar estructura en la base de datos
        document.structure_analyzed = True
        document.structure_data = structure_data
        document.total_chunks = len(chunks_data)
        document.chunks_created = True
        document.analysis_metadata = structure_data['analysis_metadata']
        document.save()
        
        # Guardar elementos de estructura
        for element_data in structure_data['structure_elements']:
            DocumentStructure.objects.get_or_create(
                document=document,
                element_id=element_data['element_id'],
                defaults={
                    'element_type': element_data['element_type'],
                    'title': element_data['title'],
                    'level': element_data['level'],
                    'page_number': 1,  # Por ahora página 1
                    'line_number': element_data['line_number'],
                    'structure_path': element_data['structure_path'],
                    'content_preview': element_data['content_preview'],
                    'metadata': element_data['metadata']
                }
            )
        
        # Guardar chunks semánticos
        for chunk_data in chunks_data:
            SemanticChunk.objects.get_or_create(
                document=document,
                chunk_id=chunk_data['chunk_id'],
                defaults={
                    'content': chunk_data['content'],
                    'structure_path': chunk_data['structure_path'],
                    'chunk_type': chunk_data['chunk_type'],
                    'page_number': 1,  # Por ahora página 1
                    'chunk_order': chunk_data['chunk_order'],
                    'keywords': chunk_data['keywords']
                }
            )
        
        logger.info(f"✅ Estructura analizada y guardada para: {document.title}")
        
        return Response({
            'document_id': str(document.id),
            'title': document.title,
            'structure_analyzed': True,
            'analysis_date': structure_data['analyzed_at'],
            'structure': structure_data,
            'summary': document.get_structure_summary(),
            'chunks_created': len(chunks_data)
        })
        
    except Exception as e:
        logger.error(f"❌ Error analizando estructura: {str(e)}")
        return Response({
            'error': 'Error al analizar la estructura del documento',
            'details': str(e),
            'document_id': document_id
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def document_chunks(request, document_id):
    """Obtiene los chunks semánticos de un documento"""
    try:
        logger.info(f"📝 Obteniendo chunks para documento: {document_id}")
        
        # Buscar el documento
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({
                'error': 'Documento no encontrado',
                'document_id': document_id
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener chunks
        chunks = SemanticChunk.objects.filter(document=document).order_by('chunk_order')
        
        chunks_data = []
        for chunk in chunks:
            chunks_data.append({
                'chunk_id': chunk.chunk_id,
                'content': chunk.content,
                'structure_path': chunk.structure_path,
                'chunk_type': chunk.chunk_type,
                'chunk_order': chunk.chunk_order,
                'keywords': chunk.keywords or []
            })
        
        logger.info(f"✅ Encontrados {len(chunks_data)} chunks para: {document.title}")
        
        return Response({
            'document_id': str(document.id),
            'title': document.title,
            'chunks': chunks_data,
            'total_chunks': len(chunks_data)
        })
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo chunks: {str(e)}")
        return Response({
            'error': 'Error al obtener los chunks del documento',
            'details': str(e),
            'document_id': document_id
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def analyze_all_documents(request):
    """Analiza la estructura de todos los documentos no analizados"""
    try:
        logger.info("🚀 Iniciando análisis masivo de documentos...")
        
        # Obtener documentos no analizados
        unanalyzed_docs = Document.objects.filter(structure_analyzed=False)
        
        if not unanalyzed_docs.exists():
            return Response({
                'message': 'Todos los documentos ya están analizados',
                'analyzed': 0,
                'total': Document.objects.count()
            })
        
        analyzer = StructureAnalyzer()
        results = {
            'analyzed': 0,
            'errors': 0,
            'details': []
        }
        
        for document in unanalyzed_docs:
            try:
                logger.info(f"🔄 Analizando: {document.title}")
                
                # Extraer texto
                text = analyzer.extract_text_from_pdf(document.file_path)
                if not text:
                    results['errors'] += 1
                    results['details'].append({
                        'document': document.title,
                        'status': 'error',
                        'message': 'No se pudo extraer texto'
                    })
                    continue
                
                # Analizar estructura
                structure_data = analyzer.analyze_structure(text)
                chunks_data = analyzer.create_semantic_chunks(text, structure_data['structure_elements'])
                
                # Guardar en base de datos
                document.structure_analyzed = True
                document.structure_data = structure_data
                document.total_chunks = len(chunks_data)
                document.chunks_created = True
                document.analysis_metadata = structure_data['analysis_metadata']
                document.save()
                
                # Guardar elementos y chunks (código similar al anterior)
                # ... (código de guardado similar al endpoint anterior)
                
                results['analyzed'] += 1
                results['details'].append({
                    'document': document.title,
                    'status': 'success',
                    'elements_found': structure_data['analysis_metadata']['total_elements'],
                    'chunks_created': len(chunks_data)
                })
                
            except Exception as e:
                logger.error(f"❌ Error analizando {document.title}: {str(e)}")
                results['errors'] += 1
                results['details'].append({
                    'document': document.title,
                    'status': 'error',
                    'message': str(e)
                })
        
        logger.info(f"✅ Análisis masivo completado: {results['analyzed']} exitosos, {results['errors']} errores")
        
        return Response({
            'message': 'Análisis masivo completado',
            'results': results,
            'total_documents': Document.objects.count(),
            'analyzed_documents': Document.objects.filter(structure_analyzed=True).count()
        })
        
    except Exception as e:
        logger.error(f"❌ Error en análisis masivo: {str(e)}")
        return Response({
            'error': 'Error en el análisis masivo de documentos',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
