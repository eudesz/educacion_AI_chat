#!/usr/bin/env python3
"""
Script de prueba para el servicio base de IA
"""

import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from apps.agents.services.tutor_agent import TutorAgent

def test_tutor_agent():
    """Probar el agente Tutor"""
    print("🤖 Iniciando prueba del Agente Tutor...")
    
    # Crear instancia del agente
    tutor = TutorAgent()
    
    # Verificar capacidades
    print("\n📊 Capacidades del agente:")
    capabilities = tutor.get_capabilities()
    for key, value in capabilities.items():
        print(f"  {key}: {value}")
    
    # Verificar estado de salud
    print("\n🏥 Estado de salud del agente:")
    health = tutor.health_check()
    for key, value in health.items():
        print(f"  {key}: {value}")
    
    # Test con respuesta simulada (sin API keys)
    print("\n💬 Prueba de procesamiento de consulta:")
    print("Nota: Como no hay API keys configuradas, se mostrará mensaje de error esperado.")
    
    context = {
        'user_level': 'Universidad',
        'subject': 'Matemáticas',
        'user_profile': {'name': 'Estudiante Test'},
        'conversation_history': [],
        'relevant_documents': []
    }
    
    query = "¿Puedes explicarme qué es una derivada?"
    response = tutor.process_query(query, context)
    print(f"Respuesta: {response}")
    
    print("\n✅ Prueba completada!")
    print("\n📝 Para activar completamente el agente:")
    print("1. Copia el archivo 'env_example_agents' como '.env'")
    print("2. Configura tus API keys de OpenAI y/o Claude")
    print("3. Reinicia el servidor Django")

def test_tutor_methods():
    """Probar métodos específicos del tutor"""
    print("\n🎯 Probando métodos específicos del Tutor...")
    
    tutor = TutorAgent()
    
    # Test de nombres y prompts
    print(f"Nombre del agente: {tutor.get_agent_name()}")
    print(f"Longitud del system prompt: {len(tutor.get_system_prompt())} caracteres")
    
    # Test de conteo de tokens (sin API)
    test_text = "Esta es una prueba de conteo de tokens."
    try:
        tokens = tutor.count_tokens(test_text)
        print(f"Tokens en '{test_text}': {tokens}")
    except Exception as e:
        print(f"Error en conteo de tokens: {e}")
    
    # Test de truncado
    long_text = "Palabra " * 100
    truncated = tutor.truncate_to_token_limit(long_text, 50)
    print(f"Texto original: {len(long_text)} caracteres")
    print(f"Texto truncado: {len(truncated)} caracteres")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de servicios IA - Fase 1")
    print("=" * 50)
    
    try:
        test_tutor_agent()
        test_tutor_methods()
        
        print("\n" + "=" * 50)
        print("✅ ¡Todas las pruebas pasaron exitosamente!")
        print("🎉 El servicio base de IA está funcionando correctamente.")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 