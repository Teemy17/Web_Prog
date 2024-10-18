from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import BTrees.OOBTree
import ZODB, ZODB.FileStorage
from z_enrollment import *
import transaction

app = FastAPI()

# Open ZODB connection
storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Temporary storage for logged in student_id
current_student_id = None

@app.get("/login", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <head>
            <title>Login Page</title>
        </head>
        <body>
            <h2>Login</h2>
            <form action="/login" method="post">
                <label for="username">Username (Student ID):</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    """

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    global current_student_id
    try:
        student_id = int(username)
    except ValueError:
        return JSONResponse(content={"error": "Invalid student ID"}, status_code=400)

    students = root.students

    if student_id in students:
        student = students[student_id]
        if student.password == password:
            current_student_id = student_id
            return RedirectResponse(url="/success", status_code=302)
        else:
            return JSONResponse(content={"error": "Incorrect login"}, status_code=401)
    else:
        return JSONResponse(content={"error": "Incorrect login"}, status_code=401)

@app.get("/success", response_class=HTMLResponse)
async def success_page():
    global current_student_id
    students = root.students
    enrollments = root.enrollments

    if current_student_id is None or current_student_id not in students:
        return JSONResponse(content={"error": "No student logged in"}, status_code=400)

    student = students[current_student_id]
    student_enrollments = [e for e in enrollments.values() if e.student == student]

    form_html = f"""
    <html>
        <head>
            <title>Transcript entry Form</title>
        </head>
        <body>
            <h2>Transcript entry Form</h2>
            <h2>Student ID: {student.id}</h2>
            <h2>Student Name: {student.name}</h2>
            <form action="/submit_scores" method="post">
    """
    
    # Dynamically create form inputs for each course
    for enrollment in student_enrollments:
        form_html += f"""
            <label for="course_{enrollment.course.id}">{enrollment.course.name} (Course ID: {enrollment.course.id}) (Credits: {enrollment.course.credit}) Score: </label>
            <input type="number" id="course_{enrollment.course.id}" name="course_{enrollment.course.id}" value="{enrollment.score}"><br><br>
        """
    
    form_html += """
            <input type="submit" value="Submit Scores">
            </form>
        </body>
    </html>
    """
    
    return HTMLResponse(content=form_html)

@app.post("/submit_scores")
async def submit_scores(request: Request):
    global current_student_id
    students = root.students
    enrollments = root.enrollments

    if current_student_id is None or current_student_id not in students:
        return JSONResponse(content={"error": "No student logged in"}, status_code=400)

    student = students[current_student_id]
    student_enrollments = [e for e in enrollments.values() if e.student == student]
    form_data = await request.form()

    # Update the scores based on form input
    for enrollment in student_enrollments:
        score_key = f"course_{enrollment.course.id}"
        if score_key in form_data:
            new_score = int(form_data[score_key])
            enrollment.score = new_score  # Update the score in ZODB
    
    # Commit changes to the database
    transaction.commit()

    # Redirect to a success page
    return RedirectResponse(url="/confirmation", status_code=302)

@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page():
    global current_student_id
    students = root.students
    enrollments = root.enrollments

    if current_student_id is None or current_student_id not in students:
        return JSONResponse(content={"error": "No student logged in"}, status_code=400)

    student = students[current_student_id]
    student_enrollments = [e for e in enrollments.values() if e.student == student]
    gpa = student.calcGrade()  # Calculate GPA

    confirmation_html = f"""
    <html>
        <head>
            <title>Submission Success</title>
        </head>
        <body>
            <h2>Student ID: {student.id}</h2>
            <h2>Student Name: {student.name}</h2>
            <h3>Transcript</h3>
            <table>
                <tr>
                    <th>Course</th>
                    <th>Score</th>
                    <th>Grade</th>
                    <th>Credits</th>
                </tr>
    """

    for enrollment in student_enrollments:
        course_name = enrollment.course.name
        score = enrollment.score
        grade = enrollment.getGrade()  # Use the grading function
        credits = enrollment.course.credit
        confirmation_html += f"""
                <tr>
                    <td>{course_name}</td>
                    <td>{score}</td>
                    <td>{grade}</td>
                    <td>{credits}</td>
                </tr>
        """

    confirmation_html += f"""
            </table>
            <h3>Total GPA: {gpa:.2f}</h3>
        </body>
    </html>
    """

    return HTMLResponse(content=confirmation_html)

grading = [
    {"Grade": "A", "min": 80, "max": 100},
    {"Grade": "B", "min": 70, "max": 79},
    {"Grade": "C", "min": 60, "max": 69},
    {"Grade": "D", "min": 50, "max": 59},
    {"Grade": "F", "min": 0, "max": 49}
]
#add data
root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Math", 4, grading)
root.courses[102] = Course(102, "Physics", 4, grading)
root.courses[103] = Course(103, "Chemistry", 5, grading)
root.courses[104] = Course(104, "Cooking", 3, grading)

# (self, enrolls, id, name=""):
root.students = BTrees.OOBTree.BTree()
root.students[1] = Student([], 1, "Alice", "password")
root.students[2] = Student([], 2, "Bob")
root.students[3] = Student([], 3, "Charlie")
root.enrollments = BTrees.OOBTree.BTree()
root.enrollments[1] = Enrollment(root.courses[101], root.students[1], 75)
root.enrollments[2] = Enrollment(root.courses[102], root.students[1], 81)
root.enrollments[3] = Enrollment(root.courses[103], root.students[1], 81)
root.enrollments[4] = Enrollment(root.courses[104], root.students[1], 57)

root.enrollments[5] = Enrollment(root.courses[101], root.students[2], 70)
root.enrollments[6] = Enrollment(root.courses[102], root.students[2], 70)
root.enrollments[7] = Enrollment(root.courses[103], root.students[2], 70)

root.enrollments[8] = Enrollment(root.courses[101], root.students[3], 60)
root.enrollments[9] = Enrollment(root.courses[102], root.students[3], 60)
root.enrollments[10] = Enrollment(root.courses[103], root.students[3], 60)

root.students[1].enrollCourse(root.enrollments[1])
root.students[1].enrollCourse(root.enrollments[2])
root.students[1].enrollCourse(root.enrollments[3])
root.students[1].enrollCourse(root.enrollments[4])

root.students[2].enrollCourse(root.enrollments[5])
root.students[2].enrollCourse(root.enrollments[6])
root.students[2].enrollCourse(root.enrollments[7])

root.students[3].enrollCourse(root.enrollments[8])
root.students[3].enrollCourse(root.enrollments[9])
root.students[3].enrollCourse(root.enrollments[10])