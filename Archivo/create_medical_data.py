#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

import datetime

def create_medical_documents():
    """Crear documentos médicos de ejemplo para análisis de tiroides"""
    
    # Datos de ejemplo para análisis de tiroides
    medical_documents = [
        {
            'filename': 'analisis_tiroides_2024-01-15.txt',
            'content': '''LABORATORIO CLÍNICO SALUSCLOUD
Fecha: 15 de enero de 2024
Paciente: Demo User

PERFIL TIROIDEO COMPLETO

TSH (Hormona Estimulante del Tiroides): 2.8 mUI/L
Rango normal: 0.4 - 4.0 mUI/L

T4 Libre (Tiroxina libre): 1.3 ng/dL  
Rango normal: 0.8 - 1.8 ng/dL

T3 Libre (Triyodotironina libre): 3.1 pg/mL
Rango normal: 2.3 - 4.2 pg/mL

T4 Total: 8.2 μg/dL
Rango normal: 5.0 - 12.0 μg/dL

Anticuerpos anti-TPO: 12 UI/mL
Rango normal: <35 UI/mL

Anticuerpos anti-tiroglobulina: 8 UI/mL
Rango normal: <20 UI/mL

INTERPRETACIÓN:
Función tiroidea normal. Todos los valores se encuentran dentro de los rangos de referencia.
No se evidencian signos de hipotiroidismo o hipertiroidismo.
Los anticuerpos tiroideos están en niveles normales, descartando tiroiditis autoinmune.

Recomendaciones:
- Control anual de función tiroidea
- Mantener dieta balanceada rica en yodo
- Seguimiento médico rutinario'''
        },
        {
            'filename': 'analisis_tiroides_2024-06-20.txt',
            'content': '''LABORATORIO CLÍNICO SALUSCLOUD
Fecha: 20 de junio de 2024
Paciente: Demo User

CONTROL SEMESTRAL - PERFIL TIROIDEO

TSH (Hormona Estimulante del Tiroides): 3.2 mUI/L
Rango normal: 0.4 - 4.0 mUI/L

T4 Libre (Tiroxina libre): 1.1 ng/dL  
Rango normal: 0.8 - 1.8 ng/dL

T3 Libre (Triyodotironina libre): 2.9 pg/mL
Rango normal: 2.3 - 4.2 pg/mL

T4 Total: 7.8 μg/dL
Rango normal: 5.0 - 12.0 μg/dL

Anticuerpos anti-TPO: 15 UI/mL
Rango normal: <35 UI/mL

INTERPRETACIÓN:
Función tiroidea dentro de límites normales. Se observa leve incremento en TSH comparado con análisis anterior (2.8 → 3.2 mUI/L), pero aún dentro del rango normal.

T4 libre y T3 libre mantienen valores adecuados.

Evolución favorable sin signos de disfunción tiroidea.

Recomendaciones:
- Continuar controles semestrales
- Mantener estilo de vida saludable
- Próximo control en 6 meses'''
        },
        {
            'filename': 'analisis_tiroides_2024-12-10.txt',
            'content': '''LABORATORIO CLÍNICO SALUSCLOUD
Fecha: 10 de diciembre de 2024
Paciente: Demo User

PERFIL TIROIDEO - CONTROL ANUAL

TSH (Hormona Estimulante del Tiroides): 4.2 mUI/L ⚠️
Rango normal: 0.4 - 4.0 mUI/L

T4 Libre (Tiroxina libre): 0.9 ng/dL  
Rango normal: 0.8 - 1.8 ng/dL

T3 Libre (Triyodotironina libre): 2.4 pg/mL
Rango normal: 2.3 - 4.2 pg/mL

T4 Total: 6.5 μg/dL
Rango normal: 5.0 - 12.0 μg/dL

Anticuerpos anti-TPO: 18 UI/mL
Rango normal: <35 UI/mL

INTERPRETACIÓN:
TSH ligeramente elevado por encima del límite superior normal (4.2 vs 4.0 mUI/L).
T4 libre y T3 libre en límite inferior del rango normal.
Esta combinación sugiere inicio de hipotiroidismo subclínico.

TENDENCIA (últimos 12 meses):
- Enero 2024: TSH 2.8 → Junio 2024: TSH 3.2 → Diciembre 2024: TSH 4.2
- Progresión ascendente de TSH indica deterioro gradual de la función tiroidea

Recomendaciones:
⚠️ SEGUIMIENTO MÉDICO INMEDIATO
- Repetir análisis en 6-8 semanas
- Evaluar inicio de tratamiento con levotiroxina
- Control nutricional (ingesta de yodo)
- Seguimiento estrecho de síntomas'''
        }
    ]
    
    # Crear directorio de documentos si no existe
    import os
    documents_dir = 'documents'
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)
    
    # Escribir los documentos
    for doc in medical_documents:
        filepath = os.path.join(documents_dir, doc['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc['content'])
        print(f"✅ Creado: {doc['filename']}")
    
    print(f"\n🎉 Se crearon {len(medical_documents)} documentos médicos de ejemplo")
    print("📊 Datos incluidos:")
    print("  - Análisis de tiroides (TSH, T4, T3)")
    print("  - Evolución temporal (enero-diciembre 2024)")
    print("  - Progresión hacia hipotiroidismo subclínico")
    print("  - Interpretaciones médicas detalladas")

if __name__ == '__main__':
    create_medical_documents() 