from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grundschule Timetabler")

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/teachers", response_model=list[schemas.Teacher])
def read_teachers(db: Session = Depends(get_db)):
    return crud.get_teachers(db)

@app.post("/teachers", response_model=schemas.Teacher)
def add_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, teacher)

@app.get("/rooms", response_model=list[schemas.Room])
def read_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)

@app.post("/rooms", response_model=schemas.Room)
def add_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)
