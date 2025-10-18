from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, date
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/") # Valor por defecto para desarrollo local
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Email configuration
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "") # Si no hay clave, la funcionalidad de correo no funcionará
NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL', 'Yuenortiz252@gmail.com')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'birthday@emergent.com')

# Scheduler for hourly birthday notifications
scheduler = BackgroundScheduler(timezone=pytz.UTC)

# MongoDB connection
mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/") # Valor por defecto para desarrollo local
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get("DB_NAME", "lleyi_default_db")] # Valor por defecto para desarrollo local

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class BirthdayComment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    person_name: str
    year: int  # año del cumpleaños
    age: int   # edad en ese cumpleaños
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BirthdayCommentCreate(BaseModel):
    person_name: str
    year: int
    age: int
    comment: str

class BirthdayCommentUpdate(BaseModel):
    comment: str

class PersonData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    birth_date: str  # formato: YYYY-MM-DD
    start_date: str  # formato: YYYY-MM-DD
    photo_url: Optional[str] = None
    show_photo: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PersonDataCreate(BaseModel):
    name: str
    birth_date: str
    start_date: str
    photo_url: Optional[str] = None
    show_photo: bool = False

class DateCheckResponse(BaseModel):
    is_birthday: bool
    today: str
    birthday_date: str
    can_edit: bool
    message: str

class EmailNotification(BaseModel):
    email: str
    person_name: str


# Helper function to check if today is the birthday
def check_is_birthday(birth_date_str: str) -> tuple[bool, date]:
    """Verifica si hoy es el cumpleaños (12 de octubre)"""
    today = date.today()
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    
    # Verificar si hoy es 12 de octubre
    is_birthday = (today.month == birth_date.month and today.day == birth_date.day)
    
    return is_birthday, today


# Birthday Person Routes
@api_router.post("/birthday/person", response_model=PersonData)
async def create_or_update_person(input: PersonDataCreate):
    """Crear o actualizar datos de una persona"""
    # Verificar si ya existe
    existing = await db.birthday_persons.find_one({"name": input.name}, {"_id": 0})
    
    if existing:
        # Actualizar
        update_data = input.model_dump()
        await db.birthday_persons.update_one(
            {"name": input.name},
            {"$set": update_data}
        )
        result = await db.birthday_persons.find_one({"name": input.name}, {"_id": 0})
        if isinstance(result['created_at'], str):
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        return PersonData(**result)
    else:
        # Crear nuevo
        person_obj = PersonData(**input.model_dump())
        doc = person_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.birthday_persons.insert_one(doc)
        return person_obj

@api_router.get("/birthday/person/{name}", response_model=PersonData)
async def get_person(name: str):
    """Obtener datos de una persona"""
    person = await db.birthday_persons.find_one({"name": name}, {"_id": 0})
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    if isinstance(person['created_at'], str):
        person['created_at'] = datetime.fromisoformat(person['created_at'])
    
    return PersonData(**person)


# Birthday Comment Routes
@api_router.post("/birthday/comment", response_model=BirthdayComment)
async def create_or_update_comment(input: BirthdayCommentCreate):
    """Crear o actualizar comentario de cumpleaños (solo si es 12 de octubre, excepto edad 17)"""
    # Obtener datos de la persona
    person = await db.birthday_persons.find_one({"name": input.person_name}, {"_id": 0})
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found. Please create person data first.")
    
    # EXCEPCIÓN ESPECIAL: El cumpleaños de 17 años se puede editar siempre
    if input.age == 17:
        # Permitir editar sin restricción de fecha
        pass
    else:
        # Verificar si hoy es el cumpleaños (12 de octubre)
        is_birthday, today = check_is_birthday(person['birth_date'])
        
        if not is_birthday:
            raise HTTPException(
                status_code=403, 
                detail=f"Solo puedes editar comentarios el 12 de octubre. Hoy es {today.strftime('%d de %B')}"
            )
        
        # Verificar que el año corresponda al año actual
        if input.year != today.year:
            raise HTTPException(
                status_code=403,
                detail=f"Solo puedes editar el comentario del año actual ({today.year})"
            )
    
    # Verificar si ya existe un comentario para este año
    existing = await db.birthday_comments.find_one(
        {"person_name": input.person_name, "year": input.year},
        {"_id": 0}
    )
    
    if existing:
        # Actualizar comentario existente
        await db.birthday_comments.update_one(
            {"person_name": input.person_name, "year": input.year},
            {"$set": {
                "comment": input.comment,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        result = await db.birthday_comments.find_one(
            {"person_name": input.person_name, "year": input.year},
            {"_id": 0}
        )
        if isinstance(result['created_at'], str):
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        if isinstance(result['updated_at'], str):
            result['updated_at'] = datetime.fromisoformat(result['updated_at'])
        return BirthdayComment(**result)
    else:
        # Crear nuevo comentario
        comment_obj = BirthdayComment(**input.model_dump())
        doc = comment_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.birthday_comments.insert_one(doc)
        return comment_obj

@api_router.get("/birthday/comments/{person_name}", response_model=List[BirthdayComment])
async def get_comments(person_name: str):
    """Obtener todos los comentarios de una persona"""
    comments = await db.birthday_comments.find(
        {"person_name": person_name},
        {"_id": 0}
    ).sort("year", 1).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for comment in comments:
        if isinstance(comment['created_at'], str):
            comment['created_at'] = datetime.fromisoformat(comment['created_at'])
        if isinstance(comment['updated_at'], str):
            comment['updated_at'] = datetime.fromisoformat(comment['updated_at'])
    
    return comments

@api_router.get("/birthday/check-date/{person_name}", response_model=DateCheckResponse)
async def check_birthday_date(person_name: str):
    """Verificar si hoy es el cumpleaños y si se puede editar"""
    person = await db.birthday_persons.find_one({"name": person_name}, {"_id": 0})
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    is_birthday, today = check_is_birthday(person['birth_date'])
    
    birth_date = datetime.strptime(person['birth_date'], "%Y-%m-%d").date()
    
    message = ""
    if is_birthday:
        message = f"¡Hoy es el cumpleaños! 🎉 Puedes agregar o editar el comentario de este año."
    else:
        message = f"Hoy no es el cumpleaños. Solo puedes editar el 12 de octubre."
    
    return DateCheckResponse(
        is_birthday=is_birthday,
        today=today.isoformat(),
        birthday_date=f"{birth_date.month:02d}-{birth_date.day:02d}",
        can_edit=is_birthday,
        message=message
    )


# Testing endpoint (SOLO PARA DESARROLLO)
@api_router.get("/birthday/test-comment-system")
async def test_comment_system():
    """Endpoint de prueba para verificar el sistema de comentarios"""
    return {
        "message": "Sistema de comentarios funcionando",
        "instructions": [
            "1. Solo puedes agregar/editar comentarios el 12 de octubre",
            "2. EXCEPCIÓN: El cumpleaños de 17 años se puede editar siempre",
            "3. Los comentarios se guardan permanentemente en MongoDB",
            "4. Cada comentario está asociado a un año específico"
        ],
        "current_date": date.today().isoformat(),
        "birthday_date": "10-12"
    }

@api_router.post("/birthday/send-notification")
async def send_email_notification(input: EmailNotification):
    """Enviar notificación por email (guardado en DB para registro)"""
    try:
        # Guardar registro de notificación enviada
        notification_record = {
            "id": str(uuid.uuid4()),
            "email": input.email,
            "person_name": input.person_name,
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "type": "birthday_reminder"
        }
        await db.email_notifications.insert_one(notification_record)
        
        return {
            "success": True,
            "message": f"Notificación registrada para {input.email}",
            "note": "Para envío real de emails, integrar con servicio como SendGrid o AWS SES"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Email sending function
def send_birthday_email(person_name: str, age: int):
    """Envía email de notificación de cumpleaños"""
    if not SENDGRID_API_KEY:
        logger.warning("SendGrid API key no configurada. Email no enviado.")
        return
    
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=NOTIFICATION_EMAIL,
            subject=f'🎉 ¡Cumpleaños de {person_name}! - {age} años',
            html_content=f'''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #000000, #8B00FF, #000000); padding: 40px; border-radius: 15px;">
                    <div style="background: rgba(0,0,0,0.7); padding: 30px; border-radius: 10px; border: 2px solid #8B00FF;">
                        <h1 style="color: #8B00FF; text-align: center; font-size: 32px; margin-bottom: 20px;">🎂 ¡Es el cumpleaños de {person_name}! 🎂</h1>
                        <p style="color: #ffffff; font-size: 18px; text-align: center; margin: 20px 0;">
                            Hoy {person_name} cumple <strong style="color: #6366F1;">{age} años</strong>
                        </p>
                        <p style="color: #cccccc; font-size: 16px; text-align: center; margin: 30px 0;">
                            🌹 Recuerda agregar un comentario especial sobre cómo fue la celebración.
                        </p>
                        <div style="text-align: center; margin-top: 30px;">
                            <p style="color: #8B00FF; font-size: 20px; font-weight: bold;">❤️ Te quiero ❤️</p>
                            <p style="color: #aaaaaa; font-size: 14px;">Más que a nadie en este mundo</p>
                        </div>
                    </div>
                </div>
            '''
        )
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email enviado exitosamente a {NOTIFICATION_EMAIL}. Status: {response.status_code}")
        
    except Exception as e:
        logger.error(f"Error enviando email: {str(e)}")


# Scheduled job to check and send birthday emails
async def check_and_send_birthday_notification():
    """Verifica si es el cumpleaños y envía notificación"""
    try:
        # Buscar persona en la base de datos
        person = await db.birthday_persons.find_one({"name": "Yennifer"}, {"_id": 0})
        
        if not person:
            logger.warning("Persona no encontrada en la base de datos")
            return
        
        birth_date = datetime.strptime(person['birth_date'], "%Y-%m-%d").date()
        today = date.today()
        
        # Verificar si es el cumpleaños (12 de octubre)
        if today.month == birth_date.month and today.day == birth_date.day:
            # Calcular edad actual
            age = today.year - birth_date.year
            logger.info(f"¡Es el cumpleaños! Enviando notificación. Edad: {age}")
            send_birthday_email(person['name'], age)
        
    except Exception as e:
        logger.error(f"Error en check_and_send_birthday_notification: {str(e)}")


# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Birthday Card API - ¡Feliz Cumpleaños!"}

@api_router.post("/birthday/test-email")
async def test_email():
    """Endpoint para probar el envío de email manualmente"""
    if not SENDGRID_API_KEY:
        raise HTTPException(status_code=400, detail="SendGrid API key no configurada")
    
    send_birthday_email("Yennifer", 17)
    return {"message": "Email de prueba enviado", "to": NOTIFICATION_EMAIL}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


# Start scheduler on application startup
@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación...")
    
    # Configurar notificaciones cada hora (del 0 al 23) solo el 12 de octubre
    for hour in range(24):
        scheduler.add_job(
            lambda: check_and_send_birthday_notification(),
            CronTrigger(
                month=10,  # Octubre
                day=12,    # Día 12
                hour=hour,  # Cada hora del día
                minute=0    # En el minuto 0
            ),
            id=f'birthday_notification_hour_{hour}',
            replace_existing=True
        )
    
    scheduler.start()
    logger.info("Scheduler iniciado. Notificaciones programadas para cada hora del 12 de octubre.")
    
    if not SENDGRID_API_KEY:
        logger.warning("⚠️ SENDGRID_API_KEY no configurada. Las notificaciones por email están desactivadas.")
    else:
        logger.info(f"✅ Sistema de notificaciones por email activado. Emails se enviarán a: {NOTIFICATION_EMAIL}")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    client.close()
    logger.info("Aplicación cerrada")