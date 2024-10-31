import BTrees.OOBTree # type: ignore
import ZODB, ZODB.FileStorage
import persistent

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()


class Course(persistent.Persistent):
    def __init__(self, id, name="", credit=1, gradeScheme=[]):
        self.id = id
        self.name = name
        self.credit = credit
        self.gradeScheme = gradeScheme

    def __str__(self): 
        return f"ID: {self.id}  Course: {self.name} ,Credit: {self.credit}"
    
    def setName(self, name):
        self.name = name

    def getCredit(self):
        return self.credit
     
    def scoreGrading(self, score): 
        for grade in self.gradeScheme: 
            if grade["min"] <= score <= grade["max"]: 
                return grade["Grade"]
    
    def setGradeScheme(self, gradeScheme):
        self.gradeScheme = gradeScheme

    def printDetail(self): 
        print(self.__str__()); 


class Student(persistent.Persistent):
    def __init__(self, enrolls, id, name=""):
        self.id = id
        self.name = name
        self.enrolls = enrolls

    def enrollCourse(self, course): 
        self.enrolls.append(course)

    def getEnrollment(self, course): 
        if course in self.enrolls: 
            return course
        else:
            return None

    def setName(self, name): 
        self.name = name
        
    def printTranscript(self): 
        print("Transcript")
        print(f"ID:  {self.id}  Name: {self.name}")
        print("Course list")
        for c in self.enrolls: 
            c.printDetail()
        print("Total GPA is: {:.2f}".format(self.calcGrade()))

    def calcGrade(self): 
        point = 0
        credit = 0
        for c in self.enrolls:
            temp = c.course.scoreGrading(c.score)
            grade = 0
            if temp == 'A': 
                grade = 4
            elif temp == 'B':
                grade = 3
            elif temp == 'C':
                grade = 2
            elif temp == 'D': 
                grade = 1
            else: 
                grade = 0; 
            point += grade * c.course.credit
            credit += c.course.credit
        if credit == 0: 
            return "N/A"
        return point / credit


class Enrollment(persistent.Persistent):
    def __init__(self, course, student, score=0):
        self.course = course
        self.score = score
        self.student = student

    def getCourse(self):
        return self.course
    
    def getGrade(self): 
        return self.course.scoreGrading(self.score)
    
    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score

    def __str__(self): 
        return f"\t{'ID:':<5} {self.course.id} Course: {self.course.name:<10} , Credit {self.course.credit} Score: {self.score} Grade: {self.course.scoreGrading(self.score)}"

    def printDetail(self): 
        print(self.__str__())

grading = [
    {"Grade": "A", "min": 80, "max": 100},
    {"Grade": "B", "min": 70, "max": 79},
    {"Grade": "C", "min": 60, "max": 69},
    {"Grade": "D", "min": 50, "max": 59},
    {"Grade": "F", "min": 0, "max": 49}
]

root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Computer Programming", 4, grading)
root.courses[102] = Course(102, "Web Programming", 4, grading)
root.courses[103] = Course(103, "Software Engineering Principles", 5, grading)
root.courses[104] = Course(104, "Artificial intelligent", 3, grading)

root.students = BTrees.OOBTree.BTree()
root.students[1] = Student([], 1, "Awa Subaru")

root.enrollments = BTrees.OOBTree.BTree()
root.enrollments[1] = Enrollment(root.courses[101], root.students[1], 75)
root.enrollments[2] = Enrollment(root.courses[102], root.students[1], 81)
root.enrollments[3] = Enrollment(root.courses[103], root.students[1], 81)
root.enrollments[4] = Enrollment(root.courses[104], root.students[1], 57)

root.students[1].enrollCourse(root.enrollments[1])
root.students[1].enrollCourse(root.enrollments[2])
root.students[1].enrollCourse(root.enrollments[3])
root.students[1].enrollCourse(root.enrollments[4])

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