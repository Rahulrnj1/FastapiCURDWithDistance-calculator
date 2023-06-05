from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from math import sqrt

app = FastAPI()

# Database connection
client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
teachers_collection = db["teachers"]
students_collection = db["students"]

# Hello World API
@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}

# Teacher model
class Teacher(BaseModel):
    name: str

# Student model
class Student(BaseModel):
    name: str
    teacher_id: str

# Routes for teachers
@app.post("/teachers")
def create_teacher(teacher: Teacher):
    new_teacher = {"name": teacher.name}
    result = teachers_collection.insert_one(new_teacher)
    return {"message": "Teacher created successfully", "teacher_id": str(result.inserted_id)}

@app.get("/teachers")
def get_teachers():
    teachers = teachers_collection.find()
    teachers_list = []
    for teacher in teachers:
        teacher["_id"] = str(teacher["_id"])  # Convert ObjectId to string
        teachers_list.append(teacher)
    return teachers_list


@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: str, teacher: Teacher):
    existing_teacher = teachers_collection.find_one({"_id":ObjectId(teacher_id)})
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teachers_collection.update_one({"_id": teacher_id}, {"$set": {"name": teacher.name}})
    return {"message": "Teacher updated successfully"}

@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: str):
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teacher["_id"] = str(teacher["_id"])  # Convert ObjectId to string
    return teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str):
    existing_teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teachers_collection.delete_one({"_id":ObjectId(teacher_id)})
    return {"message": "Teacher deleted successfully"}

#student

@app.post("/students")
def create_student(student: Student):
    existing_teacher = teachers_collection.find_one({"_id": ObjectId(student.teacher_id)})
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    new_student = {"name": student.name, "teacher_id": student.teacher_id}
    result = students_collection.insert_one(new_student)
    return {"message": "Student created successfully", "student_id": str(result.inserted_id)}

@app.get("/students")
def get_students():
    students = students_collection.find()
    students_list = []
    for student in students:
        student["_id"] = str(student["_id"])  # Convert ObjectId to string
        students_list.append(student)
    return students_list


@app.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    existing_student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    existing_teacher = teachers_collection.find_one({"_id": ObjectId(student.teacher_id)})
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": {"name": student.name, "teacher_id": ObjectId(student.teacher_id)}})
    return {"message": "Student updated successfully"}


@app.get("/students/{student_id}")
def get_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"]) 
    return student

@app.delete("/students/{student_id}")
def delete_teacher(student_id: str):
   existing_student = students_collection.find_one({"_id":ObjectId(student_id)})
   if not existing_student:
       raise HTTPException(status_code=404, detail="student not found")
   students_collection.delete_one({"_id":ObjectId(student_id)})
   return {"message": "Student deleted successfully"}
    
    



@app.get("/calculatedistance")
def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return {"distance": distance}




