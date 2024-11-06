from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    faces_count = Column(Integer, default=0)
    male_count = Column(Integer, default=0)
    female_count = Column(Integer, default=0)
    male_ages = Column(Float, default=0.0)  # Средний возраст мужчин
    female_ages = Column(Float, default=0.0)  # Средний возраст женщин
    
    images = relationship("Image", back_populates="task")


class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    name = Column(String, default='')
    male_count = Column(Integer, default=0)
    female_count = Column(Integer, default=0)
    male_ages = Column(Float, default=0.0)
    female_ages = Column(Float, default=0.0)
    
    task = relationship("Task", back_populates="images")
    faces = relationship("Face", back_populates="image")

class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True, index=True)
    h = Column(Integer)
    w = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    gender = Column(String)
    age = Column(Integer)
    image_id = Column(Integer, ForeignKey('images.id'))
    
    image = relationship("Image", back_populates="faces")