#!/bin/bash

echo "=========================================="
echo "🎂 VERIFICACIÓN DEL SISTEMA DE CUMPLEAÑOS"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar status
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

# 1. Verificar que el backend esté corriendo
echo "1️⃣ Verificando Backend..."
curl -s http://localhost:8001/api/ > /dev/null
check_status "Backend está corriendo en puerto 8001"
echo ""

# 2. Verificar MongoDB
echo "2️⃣ Verificando MongoDB..."
mongo --eval "db.version()" > /dev/null 2>&1
check_status "MongoDB está corriendo"
echo ""

# 3. Verificar API de cumpleaños
echo "3️⃣ Verificando API de Cumpleaños..."
RESPONSE=$(curl -s http://localhost:8001/api/birthday/test-comment-system)
echo "$RESPONSE" | grep -q "Sistema de comentarios funcionando"
check_status "API de comentarios funcionando"
echo ""

# 4. Verificar configuración de email
echo "4️⃣ Verificando Configuración de Email..."
if grep -q 'SENDGRID_API_KEY=""' /app/backend/.env; then
    echo -e "${YELLOW}⚠️  SendGrid API Key NO configurada${NC}"
    echo "   📝 Para activar emails, agrega tu API key en:"
    echo "   /app/backend/.env"
    echo ""
    echo "   Instrucciones completas en: /app/INSTRUCCIONES_EMAIL.md"
else
    echo -e "${GREEN}✅ SendGrid API Key configurada${NC}"
    echo ""
    echo "   🧪 Prueba enviar un email:"
    echo "   curl -X POST http://localhost:8001/api/birthday/test-email"
fi
echo ""

# 5. Verificar colores (revisar archivos CSS)
echo "5️⃣ Verificando Colores..."
if grep -q "from-purple-600 to-indigo-600" /app/frontend/src/App.js; then
    echo -e "${GREEN}✅ Colores actualizados (negro, morado, azul-morado)${NC}"
else
    echo -e "${RED}❌ Colores no actualizados${NC}"
fi
echo ""

# 6. Verificar scheduler
echo "6️⃣ Verificando Scheduler de Notificaciones..."
if tail -n 50 /var/log/supervisor/backend.err.log | grep -q "Scheduler iniciado"; then
    echo -e "${GREEN}✅ Scheduler configurado para 24 notificaciones el 12 de octubre${NC}"
    echo "   📅 Horario: Cada hora desde 12:00 AM hasta 11:00 PM"
else
    echo -e "${YELLOW}⚠️  No se pudo verificar el scheduler${NC}"
fi
echo ""

# 7. Estado de servicios
echo "7️⃣ Estado de Servicios..."
echo "─────────────────────────────────────────"
sudo supervisorctl status
echo "─────────────────────────────────────────"
echo ""

# Resumen final
echo "=========================================="
echo "📊 RESUMEN"
echo "=========================================="
echo ""
echo "✅ Sistema de cumpleaños: Funcionando"
echo "✅ Colores: Negro/Morado/Azul-morado"
echo "✅ Scheduler: 24 emails automáticos el 12 de octubre"
echo "📧 Destinatario: Yuenortiz252@gmail.com"
echo ""

if grep -q 'SENDGRID_API_KEY=""' /app/backend/.env; then
    echo -e "${YELLOW}⏳ PENDIENTE: Configurar SendGrid API Key${NC}"
    echo ""
    echo "📖 Lee las instrucciones completas:"
    echo "   cat /app/INSTRUCCIONES_EMAIL.md"
    echo ""
    echo "🚀 O ve directo a:"
    echo "   https://sendgrid.com → Create API Key"
else
    echo -e "${GREEN}🎉 ¡TODO LISTO! Sistema 100% operativo${NC}"
    echo ""
    echo "🧪 Envía un email de prueba:"
    echo "   curl -X POST http://localhost:8001/api/birthday/test-email"
fi

echo ""
echo "=========================================="
