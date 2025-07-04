#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.contrib.auth.models import User

def create_demo_users():
    """Crear usuarios demo para la aplicación"""
    
    # Usuario demo principal
    demo_user, created = User.objects.get_or_create(
        username='demo-user',
        defaults={
            'email': 'demo@saluscloud.com',
            'first_name': 'Demo',
            'last_name': 'User',
            'is_active': True,
        }
    )
    if created:
        demo_user.set_password('demo123')
        demo_user.save()
        print("✅ Usuario 'demo-user' creado exitosamente")
    else:
        print("ℹ️ Usuario 'demo-user' ya existe")

    # Doctor demo
    doctor_demo, created = User.objects.get_or_create(
        username='doctor-demo',
        defaults={
            'email': 'doctor@saluscloud.com',
            'first_name': 'Dr. María',
            'last_name': 'García',
            'is_active': True,
        }
    )
    if created:
        doctor_demo.set_password('doctor123')
        doctor_demo.save()
        print("✅ Usuario 'doctor-demo' creado exitosamente")
    else:
        print("ℹ️ Usuario 'doctor-demo' ya existe")

    # Admin demo
    admin_demo, created = User.objects.get_or_create(
        username='admin-demo',
        defaults={
            'email': 'admin@saluscloud.com',
            'first_name': 'Admin',
            'last_name': 'SalusCloud',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_demo.set_password('admin123')
        admin_demo.save()
        print("✅ Usuario 'admin-demo' creado exitosamente")
    else:
        print("ℹ️ Usuario 'admin-demo' ya existe")

    print("\n🎉 Usuarios demo configurados:")
    print("👤 demo-user / demo123 (Usuario regular)")
    print("👨‍⚕️ doctor-demo / doctor123 (Doctor)")
    print("🔧 admin-demo / admin123 (Administrador)")

if __name__ == '__main__':
    create_demo_users() 