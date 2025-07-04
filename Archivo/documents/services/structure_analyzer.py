"""
Servicio robusto para análisis de estructura de documentos PDF
Versión mejorada con detección de patrones educativos
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class StructureAnalyzer:
    """Analizador de estructura de documentos educativos"""
    
    def __init__(self):
        # Patrones para detectar elementos estructurales
        self.patterns = {
            'unidad': [
                r'(?i)unidad\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)unit\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)tema\s+(\d+)[:\s]*([^\n\r]+)',
            ],
            'modulo': [
                r'(?i)módulo\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)modulo\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)module\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)capítulo\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)capitulo\s+(\d+)[:\s]*([^\n\r]+)',
            ],
            'clase': [
                r'(?i)clase\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)lección\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)leccion\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)lesson\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)actividad\s+(\d+)[:\s]*([^\n\r]+)',
            ],
            'seccion': [
                r'(?i)(\d+\.\d+)[:\s]*([^\n\r]+)',
                r'(?i)sección\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)seccion\s+(\d+)[:\s]*([^\n\r]+)',
                r'(?i)section\s+(\d+)[:\s]*([^\n\r]+)',
            ]
        }
        
        # Patrones para detectar contenido especial
        self.content_patterns = {
            'objetivo': r'(?i)objetivos?[:\s]*([^\n\r]+)',
            'competencia': r'(?i)competencias?[:\s]*([^\n\r]+)',
            'contenido': r'(?i)contenidos?[:\s]*([^\n\r]+)',
            'evaluacion': r'(?i)evaluación[:\s]*([^\n\r]+)',
            'actividad': r'(?i)actividades?[:\s]*([^\n\r]+)',
        }
    
    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        """Extrae texto de un archivo PDF"""
        try:
            # Simulación de extracción de texto (en producción usar PyMuPDF)
            logger.info(f"📄 Extrayendo texto de: {file_path}")
            
            # Por ahora, simulamos con contenido de ejemplo basado en el nombre del archivo
            filename = Path(file_path).name.lower()
            
            if '1g' in filename:
                return self._get_sample_content_1g()
            elif '4g' in filename:
                return self._get_sample_content_4g()
            elif '6g' in filename:
                return self._get_sample_content_6g()
            else:
                return self._get_generic_sample_content()
                
        except Exception as e:
            logger.error(f"❌ Error extrayendo texto de {file_path}: {e}")
            return None
    
    def _get_sample_content_1g(self) -> str:
        """Contenido de ejemplo para documentos de 1er grado"""
        return """
        GUÍA DOCENTE - PRIMER GRADO
        
        UNIDAD 1: INTRODUCCIÓN AL APRENDIZAJE
        Objetivos: Desarrollar habilidades básicas de lectura y escritura
        
        MÓDULO 1: LETRAS Y SONIDOS
        Clase 1: Reconocimiento de vocales
        - Actividad 1: Identificar vocales en palabras
        - Evaluación: Ejercicios de discriminación auditiva
        
        Clase 2: Consonantes básicas
        - Contenido: Letras M, P, S, L
        - Actividad 2: Formación de sílabas
        
        MÓDULO 2: PRIMERAS PALABRAS
        Clase 3: Palabras simples
        - Objetivos: Leer palabras de dos sílabas
        - Actividad 3: Lectura guiada
        
        UNIDAD 2: NÚMEROS Y FORMAS
        
        MÓDULO 3: NÚMEROS DEL 1 AL 10
        Clase 4: Conteo básico
        - Competencia: Contar objetos hasta 10
        - Evaluación: Ejercicios prácticos
        """
    
    def _get_sample_content_4g(self) -> str:
        """Contenido de ejemplo para documentos de 4to grado"""
        return """
        GUÍA DOCENTE - CUARTO GRADO
        
        UNIDAD 1: COMPRENSIÓN LECTORA AVANZADA
        Objetivos: Desarrollar habilidades de análisis textual
        
        MÓDULO 1: TIPOS DE TEXTO
        Clase 1: Textos narrativos
        - Contenido: Estructura de cuentos y fábulas
        - Actividad 1: Análisis de personajes
        
        Clase 2: Textos informativos
        - Competencia: Extraer información principal
        - Evaluación: Resumen de textos
        
        MÓDULO 2: GRAMÁTICA INTERMEDIA
        Clase 3: Sustantivos y adjetivos
        - Objetivos: Clasificar palabras por categorías
        - Actividad 2: Construcción de oraciones
        
        UNIDAD 2: MATEMÁTICAS APLICADAS
        
        MÓDULO 3: OPERACIONES CON DECIMALES
        Clase 4: Suma y resta de decimales
        - Contenido: Algoritmos de cálculo
        - Actividad 3: Problemas contextualizados
        """
    
    def _get_sample_content_6g(self) -> str:
        """Contenido de ejemplo para documentos de 6to grado"""
        return """
        GUÍA DOCENTE - SEXTO GRADO - MATEMÁTICAS
        
        UNIDAD 1: ÁLGEBRA BÁSICA
        Objetivos: Introducir conceptos algebraicos fundamentales
        
        MÓDULO 13: ECUACIONES LINEALES
        Clase 1: Introducción a las variables
        - Contenido: Concepto de incógnita
        - Competencia: Resolver ecuaciones simples
        - Actividad 1: Ejercicios con balanzas
        
        Clase 2: Métodos de resolución
        - Objetivos: Aplicar propiedades de igualdad
        - Evaluación: Resolución de problemas
        
        MÓDULO 16: GEOMETRÍA ANALÍTICA
        Clase 3: Plano cartesiano
        - Contenido: Coordenadas y puntos
        - Actividad 2: Ubicación de puntos
        
        Clase 4: Funciones lineales
        - Competencia: Graficar funciones simples
        - Evaluación: Interpretación de gráficas
        
        UNIDAD 2: ESTADÍSTICA Y PROBABILIDAD
        
        MÓDULO 17: ANÁLISIS DE DATOS
        Clase 5: Medidas de tendencia central
        - Objetivos: Calcular media, mediana y moda
        - Actividad 3: Análisis de encuestas
        """
    
    def _get_generic_sample_content(self) -> str:
        """Contenido genérico de ejemplo"""
        return """
        DOCUMENTO EDUCATIVO
        
        UNIDAD 1: CONTENIDO PRINCIPAL
        Objetivos: Desarrollar competencias básicas
        
        MÓDULO 1: INTRODUCCIÓN
        Clase 1: Conceptos fundamentales
        - Actividad 1: Ejercicios básicos
        - Evaluación: Prueba diagnóstica
        
        SECCIÓN 1.1: Desarrollo teórico
        SECCIÓN 1.2: Aplicación práctica
        """
    
    def analyze_structure(self, text: str) -> Dict:
        """Analiza la estructura del texto"""
        logger.info("🔍 Analizando estructura del documento...")
        
        structure_elements = []
        analysis_metadata = {
            'units_found': 0,
            'modules_found': 0,
            'classes_found': 0,
            'sections_found': 0,
            'total_elements': 0
        }
        
        lines = text.split('\n')
        current_hierarchy = {'unit': None, 'module': None, 'class': None}
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            # Buscar cada tipo de elemento
            for element_type, patterns in self.patterns.items():
                for pattern in patterns:
                    match = re.match(pattern, line)
                    if match:
                        # Extraer número y título
                        if len(match.groups()) >= 2:
                            number = match.group(1)
                            title = match.group(2).strip()
                        else:
                            number = match.group(1) if match.groups() else "1"
                            title = line.strip()
                        
                        # Determinar nivel jerárquico
                        level = self._get_hierarchy_level(element_type)
                        
                        # Actualizar jerarquía actual
                        current_hierarchy = self._update_hierarchy(
                            current_hierarchy, element_type, number, title
                        )
                        
                        # Crear elemento de estructura
                        element = {
                            'element_id': f"{element_type}_{number}",
                            'element_type': element_type,
                            'title': title,
                            'level': level,
                            'line_number': line_num,
                            'structure_path': self._build_structure_path(current_hierarchy),
                            'content_preview': self._extract_content_preview(lines, line_num),
                            'metadata': {
                                'number': number,
                                'hierarchy': current_hierarchy.copy()
                            }
                        }
                        
                        structure_elements.append(element)
                        
                        # Actualizar contadores correctamente
                        if element_type == 'unidad':
                            analysis_metadata['units_found'] += 1
                        elif element_type == 'modulo':
                            analysis_metadata['modules_found'] += 1
                        elif element_type == 'clase':
                            analysis_metadata['classes_found'] += 1
                        elif element_type == 'seccion':
                            analysis_metadata['sections_found'] += 1
                        
                        analysis_metadata['total_elements'] += 1
                        
                        logger.info(f"  📋 {element_type.title()} encontrado: {title}")
                        break
        
        # Detectar contenido especial
        special_content = self._detect_special_content(text)
        
        result = {
            'structure_elements': structure_elements,
            'analysis_metadata': analysis_metadata,
            'special_content': special_content,
            'total_lines': len(lines),
            'analyzed_at': self._get_current_timestamp()
        }
        
        logger.info(f"✅ Análisis completado: {analysis_metadata['total_elements']} elementos encontrados")
        return result
    
    def _get_hierarchy_level(self, element_type: str) -> int:
        """Determina el nivel jerárquico del elemento"""
        levels = {
            'unidad': 1,
            'modulo': 2,
            'clase': 3,
            'seccion': 4
        }
        return levels.get(element_type, 5)
    
    def _update_hierarchy(self, current: Dict, element_type: str, number: str, title: str) -> Dict:
        """Actualiza la jerarquía actual"""
        new_hierarchy = current.copy()
        
        if element_type == 'unidad':
            new_hierarchy = {'unit': f"{number}: {title}", 'module': None, 'class': None}
        elif element_type == 'modulo':
            new_hierarchy['module'] = f"{number}: {title}"
            new_hierarchy['class'] = None
        elif element_type == 'clase':
            new_hierarchy['class'] = f"{number}: {title}"
        
        return new_hierarchy
    
    def _build_structure_path(self, hierarchy: Dict) -> str:
        """Construye la ruta de estructura"""
        path_parts = []
        
        if hierarchy['unit']:
            path_parts.append(f"Unidad {hierarchy['unit']}")
        if hierarchy['module']:
            path_parts.append(f"Módulo {hierarchy['module']}")
        if hierarchy['class']:
            path_parts.append(f"Clase {hierarchy['class']}")
        
        return " > ".join(path_parts) if path_parts else "Raíz"
    
    def _extract_content_preview(self, lines: List[str], start_line: int, max_lines: int = 3) -> str:
        """Extrae una vista previa del contenido"""
        preview_lines = []
        
        for i in range(start_line, min(start_line + max_lines, len(lines))):
            line = lines[i].strip()
            if line and not re.match(r'(?i)(unidad|módulo|modulo|clase|lección)', line):
                preview_lines.append(line)
        
        return "\n".join(preview_lines[:max_lines])
    
    def _detect_special_content(self, text: str) -> Dict:
        """Detecta contenido especial como objetivos, competencias, etc."""
        special_content = {}
        
        for content_type, pattern in self.content_patterns.items():
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                special_content[content_type] = matches
        
        return special_content
    
    def _get_current_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def create_semantic_chunks(self, text: str, structure_elements: List[Dict]) -> List[Dict]:
        """Crea chunks semánticos basados en la estructura"""
        logger.info("📝 Creando chunks semánticos...")
        
        chunks = []
        lines = text.split('\n')
        
        # Crear chunks por elemento de estructura
        for i, element in enumerate(structure_elements):
            start_line = element['line_number'] - 1
            
            # Determinar línea final
            if i + 1 < len(structure_elements):
                end_line = structure_elements[i + 1]['line_number'] - 1
            else:
                end_line = len(lines)
            
            # Extraer contenido del chunk
            chunk_lines = lines[start_line:end_line]
            content = '\n'.join(chunk_lines).strip()
            
            if content:
                chunk = {
                    'chunk_id': f"chunk_{element['element_id']}",
                    'content': content,
                    'structure_path': element['structure_path'],
                    'chunk_type': 'content',
                    'chunk_order': i + 1,
                    'element_type': element['element_type'],
                    'keywords': self._extract_keywords(content)
                }
                
                chunks.append(chunk)
        
        logger.info(f"✅ Creados {len(chunks)} chunks semánticos")
        return chunks
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extrae palabras clave del contenido"""
        # Palabras comunes a ignorar
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le',
            'da', 'su', 'por', 'son', 'con', 'para', 'las', 'del', 'los', 'una', 'al', 'como'
        }
        
        # Extraer palabras
        words = re.findall(r'\b[a-záéíóúñ]{3,}\b', content.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Contar frecuencias y tomar las más comunes
        from collections import Counter
        word_counts = Counter(keywords)
        
        return [word for word, count in word_counts.most_common(10)] 