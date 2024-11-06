from sqlalchemy.orm import Session
from fast_api_stuff.models import Task, Image, Face
from fast_api_stuff.database import get_db
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import fast_api_stuff.shms as schemas
import fast_api_stuff.models as models
import fast_api_stuff.database as database

from fast_api_stuff.parse import detect_faces, faces_parse_unfold

from dotenv import load_dotenv
import os


load_dotenv()

BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

security = HTTPBasic()

# Проверка basic auth
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = BASIC_AUTH_USERNAME
    correct_password = BASIC_AUTH_PASSWORD

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials.",
            headers={"WWW-Authenticate": "Basic"},
        )


# Добавление новой задачи
@app.put("/task/add_task/", response_model=schemas.Task,)
def create_task(
    db: Session = Depends(database.get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
    ):
    db_task = models.Task()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Удаление задачи
@app.delete("/task/{task_id}/delete_task/", response_model=None)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
    ):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # Удаляем связанные изображения и лица
    for image in task.images:
        for face in image.faces:
            db.delete(face)
        db.delete(image)
    
    db.delete(task)
    db.commit()

    return {"message": f"Task {task_id} deleted successfully"}

# Добавление изображения в задачу
@app.put("/task/{task_id}/add_image")
def add_image_to_task(task_id: int,
                    file_location: str,
                    name: str,
                    db: Session = Depends(get_db),
                    credentials: HTTPBasicCredentials = Depends(authenticate)
                    ):
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    
    if not os.path.exists(file_location):
        return {"error": "File not found"}
    
    facecloud_response = detect_faces(file_location)
    if not facecloud_response:
        raise HTTPException(status_code=500, detail="Face detection failed")

    faces_parse, stat = faces_parse_unfold(facecloud_response, name)

    image = models.Image(
        task_id = task_id,
        name = name,
        male_count = stat['male_count'],
        female_count = stat['female_count'],
        male_ages = stat['male_ages'],
        female_ages = stat['female_ages']
        )
    
    db.add(image)
    db.commit()

    faces = faces_parse['faces']
    for face_data in faces: 
        face = Face(
            image_id=image.id,
            x = face_data['bbox']['x'],
            y = face_data['bbox']['y'],
            w = face_data['bbox']['w'],
            h = face_data['bbox']['h'],
            gender = face_data['gender'],
            age = face_data['age']
        )
        db.add(face)
    
    db.commit()

    calculate_and_update_task_statistics(task_id, db)

    return {"message": "Image and faces added successfully"}
    
# Получение задачи со всеми данными
@app.get("/task/{task_id}/get")
def get_task_with_details(
    task_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate)
    ):
    task = db.query(Task).filter(Task.id == int(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Формируем структуру ответа, включающую изображения и лица
    task_details = {
        "task_id": task.id,
        "images": []
    }
    
    # Перебираем все изображения в задаче
    for image in task.images:
        image_data = {
            "image_id": image.id,
            "name": image.name,
            "faces": []
        }
        
        # Перебираем все лица на изображении
        for face in image.faces:
            face_data = {
                "face_id": face.id,
                "bounding_box": {
                    'x': face.x,
                    'y': face.y,
                    'w': face.w,
                    'h': face.h
                },
                "gender": face.gender,
                "age": face.age
            }
            image_data["faces"].append(face_data)
        
        task_details["images"].append(image_data)
    
    task_details['stat'] = {
        'faces_count': task.faces_count,
        'male_count': task.male_count,
        'female_count': task.female_count,
        'male_ages': task.male_ages,
        'female_ages': task.female_ages 
    }
    
    return task_details

# Обновление статистики
def calculate_and_update_task_statistics(
        task_id: int,
        db: Session
        ):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError("Task not found")

    images: List[Image] = db.query(Image).filter(Image.task_id == task_id).all()

    total_faces = 0
    male_count = 0
    female_count = 0
    total_male_age = 0
    total_female_age = 0

    for image in images:
        total_faces += image.male_count + image.female_count
        male_count += image.male_count
        female_count += image.female_count
        total_male_age += image.male_count * image.male_ages
        total_female_age += image.female_count * image.female_ages


    average_male_age = total_male_age / male_count if male_count > 0 else 0
    average_female_age = total_female_age / female_count if female_count > 0 else 0

    task.faces_count = total_faces
    task.male_count = male_count
    task.female_count = female_count
    task.male_ages = average_male_age
    task.female_ages = average_female_age

    db.commit()

    return task