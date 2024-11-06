from pydantic import BaseModel
from typing import List

class FaceCreate(BaseModel):
    h: int
    w: int
    x: int
    y: int
    gender: str
    age: int

class ImageCreate(BaseModel):
    task_id: int
    name: str
    faces: List[FaceCreate]

class TaskCreate(BaseModel):
    faces_count: int
    male_count: int
    female_count: int
    male_ages: float
    female_ages: float

class Task(BaseModel):
    id: int
    faces_count: int
    male_count: int
    female_count: int
    male_ages: float
    female_ages: float
    class Config:
         from_attributes = True