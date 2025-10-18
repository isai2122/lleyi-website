# 📧 Cómo Activar las Notificaciones por Email

## 🎯 Resumen
El sistema ya está configurado para enviar **emails cada hora el 12 de octubre** (de 12:00 AM a 11:00 PM) a **Yuenortiz252@gmail.com**. Solo necesitas agregar tu API key de SendGrid.

---

## 🚀 Pasos para Activar (5 minutos)

### 1. Crear Cuenta en SendGrid (Gratis)

1. Ve a: **https://sendgrid.com**
2. Click en **"Start for Free"** (Comenzar Gratis)
3. Llena el formulario de registro:
   - Email: Tu email
   - Contraseña segura
   - Acepta términos

4. Verifica tu email (revisa tu bandeja de entrada)

### 2. Obtener API Key

1. Inicia sesión en SendGrid
2. Ve a **Settings** (Configuración) en el menú izquierdo
3. Click en **API Keys**
4. Click en **"Create API Key"**
5. Configuración:
   - Name: `Birthday Notifications` (o cualquier nombre)
   - API Key Permissions: Selecciona **"Mail Send"** → **"Full Access"**
6. Click en **"Create & View"**
7. **IMPORTANTE**: Copia la API key inmediatamente (solo la verás una vez)
   - Se ve así: `SG.xxxxxxxxxxxxxxxxxx`

### 3. Agregar la API Key a tu Aplicación

**Opción A: Si estás en desarrollo local**
```bash
# Edita el archivo /app/backend/.env
nano /app/backend/.env

# Agrega tu API key:
SENDGRID_API_KEY="SG.tu_api_key_aqui"

# Guarda y reinicia el servidor
sudo supervisorctl restart backend
```

**Opción B: Si ya desplegaste en Vercel**
1. Ve a tu proyecto en Vercel
2. Settings → Environment Variables
3. Edita `SENDGRID_API_KEY`
4. Pega tu API key
5. Redeploy el proyecto

---

## ✅ Verificar que Funciona

### Prueba 1: Verificar en los Logs
```bash
# Ver logs del backend
tail -f /var/log/supervisor/backend.err.log
```

Deberías ver:
```
✅ Sistema de notificaciones por email activado. Emails se enviarán a: Yuenortiz252@gmail.com
Scheduler iniciado. Notificaciones programadas para cada hora del 12 de octubre.
```

### Prueba 2: Enviar Email de Prueba
```bash
# Opción 1: Usando curl
curl -X POST https://TU_DOMINIO/api/birthday/test-email

# Opción 2: Desde el navegador
# Abre: https://TU_DOMINIO/api/birthday/test-email
```

Si todo está bien, recibirás un email en **Yuenortiz252@gmail.com** en menos de 1 minuto.

---

## 📅 Cómo Funciona el Sistema Automático

### Programación de Emails
- **Fecha**: Solo el **12 de octubre** de cada año
- **Frecuencia**: Cada hora (24 emails en total)
- **Horario**: 
  - 12:00 AM (medianoche)
  - 1:00 AM
  - 2:00 AM
  - ... (cada hora)
  - 11:00 PM
- **Destinatario**: Yuenortiz252@gmail.com

### Contenido del Email
Cada email incluye:
- 🎂 Título: "¡Cumpleaños de Yennifer! - [edad] años"
- Mensaje personalizado con los colores morado y azul-morado
- Recordatorio para agregar comentarios
- Mensaje de amor

### Sin Intervención
Una vez configurado, el sistema funciona **completamente automático**. No necesitas hacer nada el día del cumpleaños.

---

## 💡 Límites de SendGrid (Plan Gratuito)

- **100 emails por día** (gratis)
- El 12 de octubre usa **24 emails** (uno por hora)
- Quedan **76 emails** disponibles ese día para otros usos

---

## 🐛 Solución de Problemas

### ❌ "SENDGRID_API_KEY no configurada"
**Solución**: Agrega tu API key en el archivo `.env` como se explicó arriba.

### ❌ Los emails no llegan
1. Verifica que la API key sea correcta (no tenga espacios extra)
2. Revisa la carpeta de SPAM en Yuenortiz252@gmail.com
3. En SendGrid, ve a "Activity" para ver si los emails se enviaron
4. Verifica que `NOTIFICATION_EMAIL` sea correcto en `.env`

### ❌ Error "403 Forbidden" en SendGrid
**Causa**: La API key no tiene permisos de "Mail Send"
**Solución**: Crea una nueva API key con permisos "Full Access" para "Mail Send"

### ❌ Error de autenticación
**Causa**: API key inválida o expirada
**Solución**: 
1. Ve a SendGrid → Settings → API Keys
2. Elimina la key anterior
3. Crea una nueva
4. Actualiza en tu `.env`

---

## 📝 Ejemplo de Email que Recibirás

```
De: birthday@emergent.com
Para: Yuenortiz252@gmail.com
Asunto: 🎉 ¡Cumpleaños de Yennifer! - 17 años

[Fondo degradado negro/morado]

🎂 ¡Es el cumpleaños de Yennifer! 🎂

Hoy Yennifer cumple 17 años

🌹 Recuerda agregar un comentario especial sobre cómo fue la celebración.

❤️ Te quiero ❤️
Más que a nadie en este mundo
```

---

## 🎯 Resumen Final

### Ya Está Configurado ✅
- Sistema de scheduler funcionando
- 24 notificaciones programadas (una por hora el 12 de octubre)
- Email de destino: Yuenortiz252@gmail.com
- Colores negro/morado/azul-morado aplicados

### Solo Falta ⏳
1. Obtener API key de SendGrid (5 minutos)
2. Agregar a `/app/backend/.env`
3. Reiniciar backend: `sudo supervisorctl restart backend`
4. ¡Listo! Sistema 100% automático

---

## 📞 Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs: `tail -f /var/log/supervisor/backend.err.log`
2. Prueba el endpoint de testing: `/api/birthday/test-email`
3. Verifica Activity Feed en SendGrid

---

**Desarrollado con ❤️ para Yennifer**

*Las notificaciones automáticas comenzarán el 12 de octubre sin necesidad de hacer nada.*
