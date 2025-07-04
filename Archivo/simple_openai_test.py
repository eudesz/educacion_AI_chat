#!/usr/bin/env python3
"""
Prueba simple de OpenAI sin Django
"""
import os
from openai import OpenAI

# Cargar la API key desde el archivo .env
def load_env():
    """Cargar variables de entorno desde .env"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Error cargando .env: {e}")

def test_openai():
    """Prueba simple de OpenAI"""
    load_env()
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ No se encontró OPENAI_API_KEY")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Crear cliente simple
        client = OpenAI(api_key=api_key)
        
        # Hacer petición
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hola, ¿funcionas?"}
            ],
            max_tokens=50
        )
        
        print("✅ Conexión exitosa")
        print(f"Respuesta: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_openai() 