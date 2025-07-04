#!/usr/bin/env python3
"""
Script para probar el enrutamiento y las respuestas de múltiples agentes.
"""
import os
import django
import asyncio
from typing import List

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from apps.agents.services.agent_manager import AgentManager

# --- 10 PROMPTS DE PRUEBA ---
# Diseñados para activar diferentes agentes
PROMPTS: List[str] = [
    # 1. Tutor: Pide una explicación conceptual
    "¿Puedes explicarme qué es la 'entropía' de una forma sencilla?",
    # 2. Tutor: Pide ejercicios prácticos
    "Necesito 3 ejercicios de práctica sobre la ley de Ohm.",
    # 3. Evaluator: Pide un test
    "Quiero que me hagas un quiz de 5 preguntas sobre la capitales de Europa.",
    # 4. Evaluator: Pide una evaluación de conocimiento
    "Creo que ya entiendo la diferencia entre 'mitosis' y 'meiosis', ¿puedes ponerme a prueba para confirmarlo?",
    # 5. Counselor: Pide consejo sobre hábitos de estudio
    "Me cuesta mucho concentrarme cuando estudio en casa, ¿tienes algún consejo para mí?",
    # 6. Counselor: Pide ayuda para gestionar el estrés
    "Estoy sintiendo mucha ansiedad por los próximos exámenes, ¿cómo puedo manejarla?",
    # 7. Curriculum Planner: Pide un plan de estudio
    "Quiero aprender los conceptos básicos de la inteligencia artificial. ¿Puedes diseñarme un plan de estudio de un mes?",
    # 8. Curriculum Planner: Pide la estructura de un tema
    "¿Cuál sería la estructura ideal para una presentación sobre el impacto del cambio climático?",
    # 9. Analytics: Pide un resumen de progreso (simulado)
    "Basado en mis conversaciones anteriores, ¿en qué temas he mostrado más interés o dificultad?",
    # 10. Mixto: Petición compleja para retar al enrutador
    "Después de explicarme la Primera Guerra Mundial, créame un plan de estudio para la Segunda Guerra Mundial y luego hazme un test rápido sobre la primera."
]

async def run_tests():
    """Ejecuta la suite de pruebas contra el AgentManager."""
    print("🤖 Iniciando prueba de enrutamiento con 10 prompts...")
    print("="*80)
    
    manager = AgentManager()
    
    for i, prompt in enumerate(PROMPTS):
        print(f"\n▶️  PROMPT {i+1}/{len(PROMPTS)}: \"{prompt}\"")
        print("-" * 50)
        
        try:
            # El AgentManager se encarga de todo el proceso
            result = manager.route_query(prompt)
            
            agent_used = result.get('agent_name', 'N/A')
            response_text = result.get('response', 'Sin respuesta.')
            
            print(f"👤 Agente Seleccionado: {agent_used}")
            print(f"💬 Respuesta IA: {response_text[:250]}...") # Mostramos solo un fragmento
            
        except Exception as e:
            print(f"❌ ERROR: Ocurrió un error al procesar el prompt: {e}")
            
        print("-" * 50)

    print("\n✅ Pruebas completadas.")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(run_tests()) 