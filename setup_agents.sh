#!/bin/bash

echo "🚀 Configurando Sistema de Agentes IA..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Instalando dependencias Python...${NC}"
cd Archivo
pip3 install -r requirements.txt

echo -e "${BLUE}🔧 Configurando variables de entorno...${NC}"
if [ ! -f .env ]; then
    cp env_example .env
    echo -e "${YELLOW}⚠️  Archivo .env creado. IMPORTANTE: Configura tus API keys en .env${NC}"
    echo -e "${YELLOW}   - OPENAI_API_KEY=tu-api-key-aqui${NC}"
    echo -e "${YELLOW}   - ANTHROPIC_API_KEY=tu-api-key-aqui${NC}"
else
    echo -e "${GREEN}✅ Archivo .env ya existe${NC}"
fi

echo -e "${BLUE}🗃️  Ejecutando migraciones de Django...${NC}"
python3 manage.py migrate

echo -e "${BLUE}📁 Creando directorios necesarios...${NC}"
mkdir -p chroma_db
mkdir -p logs
mkdir -p media/documents

echo -e "${BLUE}🔍 Verificando configuración...${NC}"
python3 manage.py check --deploy

echo -e "${GREEN}🎉 ¡Configuración completada!${NC}"
echo ""
echo -e "${BLUE}📋 Próximos pasos:${NC}"
echo "1. Configurar API keys en el archivo .env"
echo "2. Ejecutar el servidor: python3 manage.py runserver 8000"
echo "3. En otra terminal, ejecutar frontend: npm run dev"
echo "4. Abrir http://localhost:3000"
echo ""
echo -e "${YELLOW}💡 Documentación completa en: FASE_2_COMPLETADA.md${NC}"
echo -e "${GREEN}🚀 ¡El sistema está listo para usar!${NC}" 