from sqlalchemy.orm import Session

from . import models, schemas

# Teacher CRUD

def get_teachers(db: Session):
    return db.query(models.Teacher).all()

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(name=teacher.name, subject=teacher.subject)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# Room CRUD

def get_rooms(db: Session):
    return db.query(models.Room).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
