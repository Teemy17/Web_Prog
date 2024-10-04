from fastapi import FastAPI

app = FastAPI()

students = {
    29: {"ID": 29, "first_name": "Awa", "last_name": "Subaru"},
    30: {"ID": 30, "first_name": "Emilia", "last_name": "Tan"},
}

@app.get("/student/{path_parameter}")
async def get_student(path_parameter: int):
    return students.get(path_parameter, {"error": "Student not found"})

@app.get("/students/all")
async def get_all_students():
    return students

@app.get("/students/{id}")
async def get_student_id(id: int):
    return students.get(id, {"error": "Student not found"})

@app.post("/students/new/")
async def create_student(student: dict):
    student_id = student["ID"]
    if student_id in students:
        return {"error": "Student ID already exists"}
    students[student_id] = student
    return students[student_id]

@app.post("/students/new/{first_name}/{last_name}/{id}")
async def create_student_path(first_name: str, last_name: str, id: int):
    if id in students:
        return {"error": "Student ID already exists"}
    students[id] = {"ID": id, "first_name": first_name, "last_name": last_name}
    return students[id]

@app.post("/students/newForm")
async def create_student_form(first_name: str, last_name: str, id: int):
    if id in students:
        return {"error": "Student ID already exists"}
    students[id] = {"ID": id, "first_name": first_name, "last_name": last_name}
    return students[id]

