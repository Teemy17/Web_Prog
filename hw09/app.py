from database import root

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