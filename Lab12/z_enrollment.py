import persistent

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
        for g in self.gradeScheme: 
            if g["min"] <= score <= g["max"]: 
                return g["Grade"]
    
    def setGradeScheme(self, gradeScheme):
        self.gradeScheme = gradeScheme

    def printDetail(self): 
        print(self.__str__()); 


class Student(persistent.Persistent):
    def __init__(self, enrolls, id, name="", password=""):
        self.id = id
        self.name = name
        self.enrolls = enrolls
        self.password = password

    def enrollCourse(self, course): 
        self.enrolls.append(course)

    def getEnrollment(self, course): 
        if course in self.enrolls: 
            return course
        else:
            return None

    def setName(self, name): 
        self.name = name
        
    def printTranscript(self): #edit
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
    
    def login(self, id, password):
        if self.id == id and self.password == password:
            return True
        return False
    


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


    