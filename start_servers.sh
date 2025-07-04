#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Chat Agent AI...${NC}"
echo "=================================="

# Función para cerrar puertos
close_ports() {
    echo -e "${YELLOW}🔍 Verificando puertos en uso...${NC}"
    
    # Buscar procesos en puertos 3000 y 8000
    FRONTEND_PIDS=$(lsof -ti:3000 2>/dev/null)
    BACKEND_PIDS=$(lsof -ti:8000 2>/dev/null)
    
    if [ ! -z "$FRONTEND_PIDS" ] || [ ! -z "$BACKEND_PIDS" ]; then
        echo -e "${RED}⚠️  Puertos ocupados. Cerrando procesos...${NC}"
        
        if [ ! -z "$FRONTEND_PIDS" ]; then
            echo "   - Cerrando frontend (puerto 3000)..."
            kill -9 $FRONTEND_PIDS 2>/dev/null
        fi
        
        if [ ! -z "$BACKEND_PIDS" ]; then
            echo "   - Cerrando backend (puerto 8000)..."
            kill -9 $BACKEND_PIDS 2>/dev/null
        fi
        
        sleep 2
        echo -e "${GREEN}✅ Puertos liberados${NC}"
    else
        echo -e "${GREEN}✅ Puertos libres${NC}"
    fi
}

# Función para verificar dependencias
check_dependencies() {
    echo -e "${YELLOW}🔍 Verificando dependencias...${NC}"
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js no está instalado${NC}"
        exit 1
    fi
    
    # Verificar Python
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python no está instalado${NC}"
        exit 1
    fi
    
    # Verificar que existe package.json
    if [ ! -f "package.json" ]; then
        echo -e "${RED}❌ package.json no encontrado. ¿Estás en el directorio correcto?${NC}"
        exit 1
    fi
    
    # Verificar que existe el directorio del backend
    if [ ! -d "Archivo" ]; then
        echo -e "${RED}❌ Directorio 'Archivo' no encontrado${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dependencias verificadas${NC}"
}

# Función para iniciar el backend
start_backend() {
    echo -e "${YELLOW}🐍 Iniciando backend Django...${NC}"
    
    cd Archivo
    
    # Activar entorno virtual si existe
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "   - Entorno virtual activado"
    else
        echo -e "${YELLOW}⚠️  No se encontró entorno virtual${NC}"
    fi
    
    # Iniciar servidor Django en background
    nohup python manage.py runserver 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    cd ..
    
    # Esperar un momento para que el servidor inicie
    sleep 3
    
    # Verificar que el backend está funcionando
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|404"; then
        echo -e "${GREEN}✅ Backend iniciado correctamente (PID: $BACKEND_PID)${NC}"
        echo "   - URL: http://localhost:8000"
        echo "   - Logs: backend.log"
    else
        echo -e "${RED}❌ Error al iniciar el backend${NC}"
        echo "   - Revisa backend.log para más detalles"
    fi
}

# Función para iniciar el frontend
start_frontend() {
    echo -e "${YELLOW}⚛️  Iniciando frontend Next.js...${NC}"
    
    # Iniciar servidor Next.js en background
    nohup npm run dev > frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # Esperar un momento para que el servidor inicie
    sleep 5
    
    # Verificar que el frontend está funcionando
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
        echo -e "${GREEN}✅ Frontend iniciado correctamente (PID: $FRONTEND_PID)${NC}"
        echo "   - URL: http://localhost:3000"
        echo "   - Logs: frontend.log"
    else
        echo -e "${RED}❌ Error al iniciar el frontend${NC}"
        echo "   - Revisa frontend.log para más detalles"
    fi
}

# Función para mostrar estado final
show_status() {
    echo ""
    echo "=================================="
    echo -e "${BLUE}📊 Estado de los servidores:${NC}"
    echo ""
    
    # Verificar backend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|404"; then
        echo -e "   Backend:  ${GREEN}✅ Funcionando${NC} - http://localhost:8000"
    else
        echo -e "   Backend:  ${RED}❌ No responde${NC}"
    fi
    
    # Verificar frontend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
        echo -e "   Frontend: ${GREEN}✅ Funcionando${NC} - http://localhost:3000"
    else
        echo -e "   Frontend: ${RED}❌ No responde${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}📝 Comandos útiles:${NC}"
    echo "   - Ver logs del backend:  tail -f backend.log"
    echo "   - Ver logs del frontend: tail -f frontend.log"
    echo "   - Parar servidores:      ./stop_servers.sh"
    echo ""
    echo -e "${GREEN}🎉 ¡Aplicación lista!${NC}"
}

# Ejecutar funciones principales
close_ports
check_dependencies
start_backend
start_frontend
show_status 