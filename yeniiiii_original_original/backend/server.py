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


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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
            "2. Los comentarios se guardan permanentemente en MongoDB",
            "3. Cada comentario está asociado a un año específico",
            "4. Para probar en otra fecha, modifica la fecha del sistema o espera al 12 de octubre"
        ],
        "current_date": date.today().isoformat(),
        "birthday_date": "10-12"
    }


# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Birthday Card API - ¡Feliz Cumpleaños!"}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()