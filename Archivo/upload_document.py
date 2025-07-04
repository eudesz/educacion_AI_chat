#!/usr/bin/env python3
"""
Script para probar la carga de múltiples documentos al sistema RAG a través de la API.
"""
import os
import requests
import time

# --- CONFIGURACIÓN ---
# Asegúrate de que el servidor de Django esté corriendo en http://localhost:8000
DJANGO_API_URL = "http://localhost:8000/api/agents/upload-file/"
DOCS_DIRECTORY = "documentos_a_subir/"
SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.docx']

def upload_document(file_path: str):
    """Sube un único documento a la API de Django."""
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo no se encuentra en la ruta: {file_path}")
        return False

    try:
        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)
            files = {'file': (file_name, f)}
            
            print(f"📤 Subiendo '{file_name}'...")
            response = requests.post(DJANGO_API_URL, files=files)
            response.raise_for_status()
            
            print(f"✅ ¡Éxito! Respuesta: {response.json().get('message')}")
            return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión subiendo '{os.path.basename(file_path)}': {e}")
        if e.response:
            try:
                print(f"   Detalles: {e.response.json()}")
            except ValueError:
                print(f"   Detalles: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado con '{os.path.basename(file_path)}': {e}")
        return False

def upload_all_documents():
    """Recorre el directorio y sube todos los archivos soportados."""
    print(f"🚀 Iniciando carga masiva desde el directorio: '{DOCS_DIRECTORY}'")
    
    if not os.path.isdir(DOCS_DIRECTORY):
        print(f"❌ Error: El directorio '{DOCS_DIRECTORY}' no existe.")
        return

    files_to_upload = [
        f for f in os.listdir(DOCS_DIRECTORY) 
        if os.path.isfile(os.path.join(DOCS_DIRECTORY, f)) and any(f.endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    ]

    if not files_to_upload:
        print("🤷 No se encontraron documentos para subir.")
        return

    total_files = len(files_to_upload)
    success_count = 0
    start_time = time.time()

    print(f"Found {total_files} documentos para procesar...")

    for i, filename in enumerate(files_to_upload):
        print(f"--- Procesando archivo {i+1}/{total_files} ---")
        file_path = os.path.join(DOCS_DIRECTORY, filename)
        if upload_document(file_path):
            success_count += 1
        time.sleep(1) # Pequeña pausa para no sobrecargar el servidor

    end_time = time.time()
    duration = end_time - start_time

    print("\n--- RESUMEN DE LA CARGA ---")
    print(f"✅ Archivos subidos con éxito: {success_count}/{total_files}")
    if total_files > success_count:
        print(f"❌ Archivos fallidos: {total_files - success_count}/{total_files}")
    print(f"⏱️ Tiempo total: {duration:.2f} segundos")
    print("🎉 Proceso de carga completado.")

if __name__ == "__main__":
    # Nos aseguramos de estar en el directorio correcto
    # para que la ruta al archivo funcione.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    upload_all_documents() 