import BTrees.OOBTree
import ZODB, ZODB.FileStorage
from z_enrollment import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

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
root.students[1] = Student([], 1, "Alice")
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