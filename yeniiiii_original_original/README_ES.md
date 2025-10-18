# 🌹 Tarjeta de Cumpleaños Animada - Yennifer

Una hermosa tarjeta de cumpleaños animada con sistema de comentarios permanentes y notificaciones.

## ✨ Características Principales

### 1. 🎬 Animación de Rosa Realista
- Animación completa de una rosa realista con pétalos, hojas y tallo
- Efectos de luz y partículas flotantes
- Transiciones suaves y elegantes
- Secuencia de animación automática al cargar la página

### 2. 💬 Sistema de Comentarios Permanentes
- **Guardado Permanente**: Los comentarios se guardan en MongoDB y nunca se borran
- **Restricción por Fecha**: Solo se pueden agregar/editar comentarios el **12 de octubre** (día del cumpleaños)
- **Comentarios por Año**: Cada cumpleaños (desde los 17 hasta los 100 años) puede tener su propio comentario
- **Validación Automática**: El sistema verifica automáticamente si hoy es el cumpleaños

### 3. 🔔 Sistema de Notificaciones
- **Notificaciones del Navegador**: Recibe alertas cuando es el cumpleaños
- **Botón de Activación**: Fácil habilitación con un solo clic
- **Múltiples Alertas**: Notificaciones al agregar comentarios y en eventos importantes

### 4. 📅 Lista de Cumpleaños
- Lista completa de todos los cumpleaños desde la edad actual hasta los 100 años
- Muestra fecha, día de la semana y edad
- Indicadores visuales para:
  - 🎁 Cumpleaños actual
  - ✅ Día que se puede editar
  - 💬 Comentarios guardados
- Scroll suave con controles de navegación

### 5. 🎨 Diseño Visual
- Gradientes rosa-violeta elegantes
- Fondo oscuro con efectos de profundidad
- Animaciones suaves en cada interacción
- Diseño responsive para móviles y tablets
- Corazones flotantes decorativos

## 🚀 Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **MongoDB**: Base de datos NoSQL para almacenamiento permanente
- **Motor**: Driver asíncrono de MongoDB
- **Pydantic**: Validación de datos

### Frontend
- **React**: Biblioteca de UI
- **Axios**: Cliente HTTP
- **Lucide React**: Iconos modernos
- **CSS3**: Animaciones personalizadas

## 📋 Estructura de la Base de Datos

### Colección: birthday_persons
```json
{
  "id": "uuid",
  "name": "Yennifer",
  "birth_date": "2008-10-12",
  "start_date": "2025-10-12",
  "photo_url": null,
  "show_photo": false,
  "created_at": "2025-10-13T..."
}
```

### Colección: birthday_comments
```json
{
  "id": "uuid",
  "person_name": "Yennifer",
  "year": 2025,
  "age": 17,
  "comment": "¡Fue un cumpleaños increíble!",
  "created_at": "2025-10-12T...",
  "updated_at": "2025-10-12T..."
}
```

## 🔌 API Endpoints

### GET `/api/`
Mensaje de bienvenida

### POST `/api/birthday/person`
Crear o actualizar datos de una persona
```json
{
  "name": "Yennifer",
  "birth_date": "2008-10-12",
  "start_date": "2025-10-12",
  "show_photo": false,
  "photo_url": null
}
```

### GET `/api/birthday/person/{name}`
Obtener datos de una persona

### POST `/api/birthday/comment`
Agregar o editar comentario (solo 12 de octubre)
```json
{
  "person_name": "Yennifer",
  "year": 2025,
  "age": 17,
  "comment": "¡Fue un día maravilloso!"
}
```

**⚠️ Restricción**: Solo funciona el 12 de octubre del año correspondiente

### GET `/api/birthday/comments/{person_name}`
Obtener todos los comentarios guardados

### GET `/api/birthday/check-date/{person_name}`
Verificar si hoy es el cumpleaños y si se puede editar

### GET `/api/birthday/test-comment-system`
Endpoint de prueba para verificar el sistema

## 🎯 Cómo Usar la Aplicación

### 1. Primera Visita
- La aplicación se carga automáticamente
- Verás la animación completa del mensaje y la rosa
- Se muestra la lista de cumpleaños del 17 al 100 años

### 2. Habilitar Notificaciones
- Haz clic en el botón "Habilitar Notificaciones" en la esquina superior derecha
- Acepta los permisos en tu navegador
- Recibirás notificaciones cuando sea el cumpleaños

### 3. Agregar Comentarios (Solo 12 de Octubre)
- **Cuando NO es 12 de octubre**: Verás el mensaje "Hoy no es el cumpleaños. Solo puedes editar el 12 de octubre"
- **Cuando SÍ es 12 de octubre**:
  1. Verás un icono ➕ verde al lado del cumpleaños actual
  2. Haz clic en el botón
  3. Escribe tu comentario sobre cómo estuvo la celebración
  4. Haz clic en "Guardar"
  5. El comentario se guarda PERMANENTEMENTE en la base de datos

### 4. Ver Comentarios Guardados
- Los comentarios guardados aparecen con un borde rosa debajo de cada fecha
- Muestra la fecha en que fue guardado
- Solo puedes editar el comentario del año actual, y solo el 12 de octubre

### 5. Reproducir Animación
- Haz clic en "Reproducir" para ver nuevamente la animación completa
- La animación incluye:
  1. Mensaje letra por letra
  2. Aparición de la rosa realista
  3. Lista de cumpleaños con efecto cascada
  4. Mensaje final de amor

## 🎨 Personalización

### Cambiar Colores
Edita `/app/frontend/src/App.css` para modificar los gradientes:
```css
.bg-gradient-to-br {
  background: linear-gradient(to bottom right, #000, #7c3aed, #000);
}
```

### Modificar Persona
Edita los valores en `/app/frontend/src/App.js`:
```javascript
const name = 'Yennifer';
const birthDateStr = '2008-10-12';
const startDateStr = '2025-10-12';
```

### Cambiar Rango de Edades
Modifica la función `generateFutureBirthdays()` en App.js:
```javascript
for (let age = currentAge; age <= 100; age++) {
  // Cambia 100 por el número que desees
}
```

## 🔐 Seguridad

- Los comentarios solo se pueden agregar/editar el 12 de octubre
- Validación de fecha en el backend
- Los datos se almacenan de forma segura en MongoDB
- No se permite modificar comentarios de años pasados

## 📱 Responsive Design

La aplicación es completamente responsive:
- **Desktop**: Diseño completo en dos columnas
- **Tablet**: Diseño adaptado con scroll horizontal
- **Mobile**: Vista única optimizada para pantalla pequeña

## 🖨️ Funcionalidad de Impresión

- Botón "Imprimir" incluido
- Las animaciones se ocultan al imprimir
- Solo se imprime la información importante (lista de cumpleaños y comentarios)

## 🐛 Solución de Problemas

### Las notificaciones no funcionan
1. Verifica que tu navegador soporte notificaciones
2. Asegúrate de haber dado permiso en la configuración del navegador
3. Haz clic en "Habilitar Notificaciones" nuevamente

### No puedo agregar comentarios
- **Causa más común**: No es 12 de octubre
- **Solución**: Espera hasta el 12 de octubre del año correspondiente
- **Nota**: Esto es por diseño, para preservar la autenticidad de los recuerdos

### La animación no se reproduce
1. Recarga la página
2. Haz clic en el botón "Reproducir"
3. Asegúrate de que JavaScript esté habilitado

### Los comentarios no se guardan
1. Verifica la conexión con el backend
2. Comprueba que MongoDB esté corriendo
3. Revisa los logs del backend: `tail -f /var/log/supervisor/backend.err.log`

## 💡 Características Futuras Planeadas

- [ ] Múltiples personas (gestión de varios cumpleaños)
- [ ] Subir fotos para cada cumpleaños
- [ ] Temas de colores personalizables
- [ ] Recordatorios por email
- [ ] Compartir tarjeta en redes sociales
- [ ] Agregar música de fondo
- [ ] Galería de fotos por año

## 📝 Notas del Desarrollador

Esta aplicación fue diseñada con amor para preservar recuerdos especiales. La restricción de edición solo el 12 de octubre es intencional, para que cada comentario sea auténtico y refleje verdaderamente cómo fue cada cumpleaños.

Los comentarios se guardan permanentemente en MongoDB y nunca se borran automáticamente, creando así un diario digital de cumpleaños que se puede consultar por años.

## 🤝 Contribuciones

Si deseas mejorar esta aplicación:
1. Haz un fork del repositorio
2. Crea una rama para tu característica
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso personal y fue creado con mucho cariño.

---

**Desarrollado con ❤️ para Yennifer** 

*"Más que a nadie en este mundo. Eres la mejor hermana que alguien podría tener."*
