from database import root
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

if __name__ == "__main__": 
    courses = root.courses
    for c in courses: 
        course = courses[c]
        course.printDetail()
    print()

    students = root.students
    for s in students: 
        student = students[s]
        student.printTranscript()
        print()
    
