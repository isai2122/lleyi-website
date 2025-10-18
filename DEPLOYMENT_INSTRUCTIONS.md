# 🚀 Instrucciones de Deployment en Vercel

## 📋 Requisitos Previos

### 1. Cuenta de SendGrid (Gratis)
1. Ve a [https://sendgrid.com](https://sendgrid.com)
2. Crea una cuenta gratuita (100 emails/día gratis)
3. Ve a Settings → API Keys
4. Crea una nueva API Key con permisos de "Mail Send"
5. Copia la API Key (solo la verás una vez)

### 2. Base de Datos MongoDB
Necesitas una base de datos MongoDB. Opciones:

#### Opción A: MongoDB Atlas (Recomendado - Gratis)
1. Ve a [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Crea cuenta gratuita
3. Crea un cluster gratuito (M0)
4. En Database Access: Crea un usuario con contraseña
5. En Network Access: Agrega tu IP o permite acceso desde cualquier lugar (0.0.0.0/0)
6. Click en "Connect" → "Connect your application"
7. Copia la connection string (formato: `mongodb+srv://usuario:password@cluster.mongodb.net/`)

#### Opción B: Railway (Alternativa)
1. Ve a [https://railway.app](https://railway.app)
2. Crea proyecto nuevo
3. Agrega MongoDB desde el marketplace
4. Copia la MONGO_URL que te proporciona

---

## 🌐 Deployment en Vercel

### Paso 1: Preparar el Proyecto

1. **Asegúrate de tener cuenta en Vercel**
   - Ve a [https://vercel.com](https://vercel.com)
   - Regístrate con GitHub (recomendado)

2. **Sube tu proyecto a GitHub**
   ```bash
   # Si aún no has inicializado git
   git init
   git add .
   git commit -m "Initial commit"
   
   # Crea un repositorio en GitHub y luego:
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

### Paso 2: Deploy en Vercel

1. **Importar Proyecto**
   - Ve a tu dashboard de Vercel
   - Click en "Add New" → "Project"
   - Importa tu repositorio de GitHub

2. **Configurar Build Settings**
   - Framework Preset: **Other**
   - Build Command: `cd frontend && yarn install && yarn build`
   - Output Directory: `frontend/build`
   - Install Command: `yarn install`

3. **Configurar Variables de Entorno**
   En la sección "Environment Variables", agrega:

   ```
   MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/birthday_db
   DB_NAME=birthday_db
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
   NOTIFICATION_EMAIL=Yuenortiz252@gmail.com
   FROM_EMAIL=birthday@emergent.com
   CORS_ORIGINS=*
   REACT_APP_BACKEND_URL=https://TU-PROYECTO.vercel.app
   ```

   **IMPORTANTE**: Reemplaza:
   - `MONGO_URL`: Tu connection string de MongoDB Atlas
   - `SENDGRID_API_KEY`: Tu API key de SendGrid
   - `REACT_APP_BACKEND_URL`: El URL de tu proyecto en Vercel (lo obtendrás después del primer deploy)

4. **Deploy**
   - Click en "Deploy"
   - Espera a que termine (2-3 minutos)

### Paso 3: Actualizar Backend URL

1. Después del primer deploy, copia tu URL de Vercel (ej: `https://yeniiiii.vercel.app`)
2. Ve a Settings → Environment Variables
3. Edita `REACT_APP_BACKEND_URL` y ponle tu URL de Vercel
4. Redeploy el proyecto (en la pestaña "Deployments", click en los 3 puntos del último deployment → "Redeploy")

---

## ⚙️ Configuración Alternativa (Sin Vercel)

### Opción 1: Railway (Recomendado para Full-Stack)

1. Ve a [https://railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente FastAPI y React
4. Agrega las mismas variables de entorno
5. Deploy automático

### Opción 2: Render

1. Ve a [https://render.com](https://render.com)
2. Crea dos servicios:
   - **Web Service** para el backend (FastAPI)
   - **Static Site** para el frontend (React)
3. Configura las variables de entorno
4. Deploy

---

## 🔧 Verificación Post-Deployment

### 1. Probar Backend
```bash
curl https://TU-PROYECTO.vercel.app/api/
# Debe responder: {"message": "Birthday Card API - ¡Feliz Cumpleaños!"}
```

### 2. Probar Email (Solo para testing)
```bash
curl -X POST https://TU-PROYECTO.vercel.app/api/birthday/test-email
# Debe enviar un email de prueba a Yuenortiz252@gmail.com
```

### 3. Verificar Sistema de Comentarios
```bash
curl https://TU-PROYECTO.vercel.app/api/birthday/test-comment-system
```

---

## 📧 Sistema de Notificaciones por Email

### Cómo Funciona

- **Automático**: El sistema envía emails **cada hora** el **12 de octubre**
- **Horario**: Desde las 12:00 AM hasta las 11:00 PM (24 notificaciones en total)
- **Destinatario**: `Yuenortiz252@gmail.com`
- **Sin intervención**: Una vez configurado, funciona automáticamente

### Verificar que esté Activo

Al iniciar el backend, verás en los logs:
```
✅ Sistema de notificaciones por email activado. Emails se enviarán a: Yuenortiz252@gmail.com
Scheduler iniciado. Notificaciones programadas para cada hora del 12 de octubre.
```

### Probar Email Manualmente

Puedes enviar un email de prueba en cualquier momento:
```bash
curl -X POST https://TU-PROYECTO.vercel.app/api/birthday/test-email
```

O desde el navegador, abre:
```
https://TU-PROYECTO.vercel.app/api/birthday/test-email
```

---

## 🎨 Esquema de Colores

La aplicación ahora usa:
- **Negro**: `#000000` - Fondo principal
- **Morado**: `#8B00FF` - Pétalos externos de la rosa
- **Azul-Morado (Índigo)**: `#6366F1` - Pétalos internos, acentos
- **Morado-Azul (Violeta)**: `#7C3AED` - Gradientes, botones

---

## 🐛 Solución de Problemas

### Los emails no llegan
1. Verifica que `SENDGRID_API_KEY` esté correcta en Vercel
2. Revisa los logs en Vercel (pestaña "Logs")
3. Verifica que el email `Yuenortiz252@gmail.com` esté correcto
4. Prueba enviar un email manual con el endpoint `/api/birthday/test-email`

### Error de conexión a MongoDB
1. Verifica que `MONGO_URL` sea correcta
2. En MongoDB Atlas, asegúrate de permitir acceso desde cualquier IP
3. Verifica que el usuario tenga permisos de lectura/escritura

### Frontend no se conecta al Backend
1. Verifica que `REACT_APP_BACKEND_URL` apunte a tu dominio de Vercel
2. Asegúrate de que el backend esté corriendo (visita `/api/`)
3. Verifica CORS en backend (.env debe tener `CORS_ORIGINS=*`)

---

## 📝 Notas Importantes

1. **SendGrid gratis**: 100 emails por día
   - El 12 de octubre se envían 24 emails (uno por hora)
   - Quedan 76 emails disponibles para otros usos ese día

2. **MongoDB Atlas gratis**: 
   - 512 MB de almacenamiento
   - Suficiente para miles de comentarios

3. **Vercel gratis**:
   - 100 GB de ancho de banda/mes
   - Más que suficiente para uso personal

4. **Backup recomendado**:
   - Exporta comentarios regularmente desde MongoDB
   - Considera hacer backup del database cada año

---

## 🎉 ¡Listo!

Tu aplicación de cumpleaños está lista y funcionando. El sistema:
- ✅ Envía emails automáticamente cada hora el 12 de octubre
- ✅ Guarda comentarios permanentemente
- ✅ Animación de rosa con colores negro/morado/azul-morado
- ✅ Lista de cumpleaños hasta los 100 años
- ✅ 100% automático, sin necesidad de intervención

---

**Desarrollado con ❤️ para Yennifer**

*Si tienes problemas, revisa los logs en Vercel o contacta a soporte.*
