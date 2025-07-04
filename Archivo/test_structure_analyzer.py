#!/usr/bin/env python
"""
Script de prueba para el analizador de estructura de documentos
"""

import os
import sys
import django
import json
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from apps.documents.services.structure_analyzer import DocumentStructureAnalyzer
from apps.documents.services.semantic_chunker import SemanticChunker

def test_structure_analyzer():
    """Prueba el analizador de estructura con documentos reales"""
    
    # Buscar documentos PDF
    docs_dir = Path("documentos_a_subir")
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No se encontraron archivos PDF en documentos_a_subir/")
        return
    
    analyzer = DocumentStructureAnalyzer()
    chunker = SemanticChunker()
    
    for pdf_file in pdf_files[:2]:  # Solo los primeros 2 para prueba
        print(f"\n{'='*60}")
        print(f"ANALIZANDO: {pdf_file.name}")
        print(f"{'='*60}")
        
        try:
            # Analizar estructura
            print("🔍 Analizando estructura...")
            structure = analyzer.analyze_pdf_structure(str(pdf_file))
            
            # Mostrar resultados
            metadata = structure.get('analysis_metadata', {})
            print(f"📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   • Total de páginas: {structure.get('total_pages', 0)}")
            print(f"   • Elementos encontrados: {metadata.get('total_elements', 0)}")
            print(f"   • Unidades: {metadata.get('units_found', 0)}")
            print(f"   • Módulos: {metadata.get('modules_found', 0)}")
            print(f"   • Clases: {metadata.get('classes_found', 0)}")
            
            # Mostrar elementos detectados
            elements = structure.get('elements', [])
            if elements:
                print(f"\n📋 ELEMENTOS DETECTADOS:")
                for element in elements[:10]:  # Solo los primeros 10
                    print(f"   • {element.element_type.upper()}: {element.title}")
                    print(f"     Página: {element.page_number}, Nivel: {element.level}")
                    if element.content_preview:
                        preview = element.content_preview[:100] + "..." if len(element.content_preview) > 100 else element.content_preview
                        print(f"     Preview: {preview}")
                    print()
            
            # Mostrar jerarquía
            hierarchy = structure.get('hierarchy', {})
            units = hierarchy.get('units', [])
            if units:
                print(f"\n🏗️ JERARQUÍA DETECTADA:")
                for unit in units:
                    print(f"   📚 UNIDAD: {unit['title']}")
                    
                    for module in unit.get('modules', []):
                        print(f"      📖 MÓDULO: {module['title']}")
                        
                        for class_data in module.get('classes', []):
                            print(f"         📝 CLASE: {class_data['title']}")
            
            # Crear chunks semánticos
            print(f"\n🧩 CREANDO CHUNKS SEMÁNTICOS...")
            # Para la prueba, usaremos contenido simulado
            sample_content = f"Contenido simulado del documento {pdf_file.name}\n" * 100
            chunks = chunker.create_semantic_chunks(sample_content, structure)
            
            print(f"   • Chunks creados: {len(chunks)}")
            
            # Mostrar algunos chunks
            if chunks:
                print(f"\n📦 CHUNKS CREADOS:")
                for chunk in chunks[:5]:  # Solo los primeros 5
                    print(f"   • {chunk.element_type.upper()}: {chunk.title}")
                    print(f"     ID: {chunk.chunk_id}")
                    print(f"     Ruta: {chunk.structure_path}")
                    print(f"     Contenido: {len(chunk.content)} caracteres")
                    print()
            
        except Exception as e:
            print(f"❌ ERROR analizando {pdf_file.name}: {str(e)}")
            import traceback
            traceback.print_exc()

def test_with_sample_text():
    """Prueba con texto de ejemplo"""
    print(f"\n{'='*60}")
    print("PRUEBA CON TEXTO DE EJEMPLO")
    print(f"{'='*60}")
    
    sample_text = """
    UNIDAD 1: Matemática Básica
    
    Introducción a los números y operaciones fundamentales.
    
    MÓDULO 1: Números Naturales
    
    En este módulo aprenderemos sobre los números naturales.
    
    CLASE 1: Conteo Básico
    
    Aprenderemos a contar del 1 al 10.
    Los números naturales son: 1, 2, 3, 4, 5...
    
    CLASE 2: Suma Simple
    
    La suma es una operación matemática básica.
    Ejemplo: 2 + 3 = 5
    
    MÓDULO 2: Operaciones
    
    Veremos las operaciones básicas.
    
    CLASE 3: Resta
    
    La resta es lo contrario de la suma.
    
    UNIDAD 2: Geometría
    
    Estudiaremos las formas geométricas.
    
    MÓDULO 3: Figuras Planas
    
    Las figuras planas tienen dos dimensiones.
    
    CLASE 4: Círculos y Cuadrados
    
    El círculo es redondo, el cuadrado tiene 4 lados iguales.
    """
    
    analyzer = DocumentStructureAnalyzer()
    chunker = SemanticChunker()
    
    try:
        # Analizar estructura del texto
        structure = analyzer.analyze_structure_from_content(sample_text)
        
        metadata = structure.get('analysis_metadata', {})
        print(f"📊 RESULTADOS:")
        print(f"   • Elementos: {metadata.get('total_elements', 0)}")
        print(f"   • Unidades: {metadata.get('units_found', 0)}")
        print(f"   • Módulos: {metadata.get('modules_found', 0)}")
        print(f"   • Clases: {metadata.get('classes_found', 0)}")
        
        # Crear chunks
        chunks = chunker.create_semantic_chunks(sample_text, structure)
        print(f"   • Chunks: {len(chunks)}")
        
        # Mostrar jerarquía
        hierarchy = structure.get('hierarchy', {})
        print(f"\n🏗️ JERARQUÍA:")
        for unit in hierarchy.get('units', []):
            print(f"   📚 {unit['title']}")
            for module in unit.get('modules', []):
                print(f"      📖 {module['title']}")
                for class_data in module.get('classes', []):
                    print(f"         📝 {class_data['title']}")
        
        # Mostrar chunks
        print(f"\n📦 CHUNKS:")
        for chunk in chunks:
            print(f"   • {chunk.title} ({chunk.element_type})")
            print(f"     Ruta: {chunk.structure_path}")
            print(f"     Contenido: {len(chunk.content)} chars")
            print()
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL ANALIZADOR DE ESTRUCTURA")
    
    # Prueba con texto de ejemplo primero
    test_with_sample_text()
    
    # Luego prueba con PDFs reales
    test_structure_analyzer()
    
    print(f"\n✅ PRUEBAS COMPLETADAS") 