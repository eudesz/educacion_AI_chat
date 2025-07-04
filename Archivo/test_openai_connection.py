#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con OpenAI
"""
import os
import django
from decouple import config

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from openai import OpenAI

def test_openai_connection():
    """Prueba la conexión con OpenAI"""
    try:
        # Obtener la API key del archivo .env
        api_key = config('OPENAI_API_KEY')
        print(f"API Key configurada: {api_key[:10]}...{api_key[-4:]}")
        
        # Inicializar cliente OpenAI
        client = OpenAI(api_key=api_key)
        
        # Hacer una consulta simple
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente educativo especializado."},
                {"role": "user", "content": "Hola, ¿puedes explicar brevemente qué es la fotosíntesis?"}
            ],
            max_tokens=150
        )
        
        print("✅ Conexión exitosa con OpenAI")
        print(f"Modelo usado: {response.model}")
        print(f"Respuesta: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la conexión: {str(e)}")
        return False

def test_agent_manager():
    """Prueba el sistema de gestión de agentes"""
    try:
        from apps.agents.services.agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Probar detección de intención
        query = "¿Puedes ayudarme a estudiar matemáticas?"
        agent = manager.route_query(query)
        print(f"✅ Query: '{query}' -> Agente: {agent}")
        
        # Probar estado de salud
        health = manager.health_check()
        print(f"✅ Estado de salud del sistema: {health}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en el sistema de agentes: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del sistema de agentes IA...")
    print("=" * 50)
    
    # Prueba 1: Conexión OpenAI
    print("\n1. Probando conexión con OpenAI...")
    openai_ok = test_openai_connection()
    
    # Prueba 2: Sistema de agentes
    print("\n2. Probando sistema de gestión de agentes...")
    agent_ok = test_agent_manager()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"OpenAI: {'✅ OK' if openai_ok else '❌ FALLO'}")
    print(f"Agentes: {'✅ OK' if agent_ok else '❌ FALLO'}")
    
    if openai_ok and agent_ok:
        print("\n🎉 ¡Sistema listo para usar!")
    else:
        print("\n⚠️  Revisar configuración.") 