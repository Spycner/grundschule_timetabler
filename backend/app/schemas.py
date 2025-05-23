from pydantic import BaseModel

class TeacherBase(BaseModel):
    name: str
    subject: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True
