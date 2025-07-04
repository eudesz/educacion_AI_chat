#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from documents.models import Document

print("🔍 VERIFICANDO DOCUMENTOS EN LA BASE DE DATOS")
print("=" * 60)

docs = Document.objects.all()
print(f"📊 Total documentos: {docs.count()}")

if docs.count() > 0:
    print("\n📄 DOCUMENTOS ENCONTRADOS:")
    for doc in docs:
        print(f"- {doc.filename}")
        print(f"  Usuario: {doc.user_id}")
        print(f"  Fecha: {doc.upload_date}")
        print(f"  Tamaño: {getattr(doc, 'file_size', 'N/A')}")
        print(f"  Ruta: {doc.file_path}")
        print()
else:
    print("\n❌ NO HAY DOCUMENTOS EN LA BASE DE DATOS")
    print("Los documentos deben subirse a través de la interfaz web.")

# Verificar usuarios
from django.contrib.auth.models import User
users = User.objects.all()
print(f"👥 Usuarios en el sistema: {users.count()}")
for user in users:
    print(f"- {user.username} ({user.first_name} {user.last_name})") 