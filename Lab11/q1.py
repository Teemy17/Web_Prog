import ZODB, ZODB.FileStorage
import persistent
import transaction
from BTrees.OOBTree import OOBTree
from z_enrollment.classes import *

# Set up the database
storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Initialize BTrees if they don't exist
if 'students' not in root:
    root['students'] = OOBTree()
if 'courses' not in root:
    root['courses'] = OOBTree()

# Create objects
course1 = Course(id=1, name="Math", credit=3)
course2 = Course(id=2, name="Science", credit=4)
course3 = Course(id=3, name="English", credit=3)
course4 = Course(id=4, name="History", credit=3)

student = Student(enrolls=[], id=1, name="John Doe")
student2 = Student(enrolls=[], id=2, name="Jane Doe")

enrollment1 = Enrollment(course=course1, grade='A', student=student)
enrollment2 = Enrollment(course=course2, grade='B', student=student)
enrollment3 = Enrollment(course=course3, grade='C', student=student2)
enrollment4 = Enrollment(course=course4, grade='D', student=student2)

student.enrollCourse(enrollment1)
student.enrollCourse(enrollment2)
student2.enrollCourse(enrollment3)
student2.enrollCourse(enrollment4)

# Store objects in BTrees
root['students'][student.id] = student
root['students'][student2.id] = student2
root['courses'][course1.id] = course1
root['courses'][course2.id] = course2
root['courses'][course3.id] = course3
root['courses'][course4.id] = course4

# Commit the transaction
transaction.commit()

# Close the connection
connection.close()
db.close()

if __name__ == "__main__":
    # Access and print course details
    for course_id in root['courses']:
        course = root['courses'][course_id]
        course.printDetail()
    print()

    # Access and print student transcript
    for student_id in root['students']:
        student = root['students'][student_id]
        student.printTranscript()
    print()
