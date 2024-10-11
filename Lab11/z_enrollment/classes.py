import persistent

class Course(persistent.Persistent):
    def __init__(self, id, name="", credit=0):
        self.id = id
        self.name = name
        self.credit = credit

    def __str__(self):
        return "ID: %8s, Course Name: %s, Credit: %d" % (str(self.id), self.name, self.credit)
    
    def setName(self, name):
        self.name = name

    def printDetail(self):
        print(self.__str__())

    def getCredit(self):
        return self.credit

class Student(persistent.Persistent):
    def __init__(self, enrolls, id, name=""):
        self.id = id
        self.name = name
        self.enrolls = enrolls

    def enrollCourse(self, course):
        self.enrolls.append(course)

    def calculateGPA(self):
        total_credits = 0
        total_grade_points = 0
        for enrollment in self.enrolls:
            course = enrollment.getCourse()
            grade = enrollment.getGrade()
            if grade == 'A':
                grade_point = 4
            elif grade == 'B':
                grade_point = 3
            elif grade == 'C':
                grade_point = 2
            elif grade == 'D':
                grade_point = 1
            elif grade == 'F':
                grade_point = 0
            else:
                grade_point = 0
            total_credits += course.getCredit()
            total_grade_points += grade_point * course.getCredit()
        
        if total_credits == 0:
            return 0.0
        return total_grade_points / total_credits

    def printTranscript(self):
        print("Student ID: %s, Name: %s" % (str(self.id), self.name))
        for enrollment in self.enrolls:
            enrollment.printDetail()
        gpa = self.calculateGPA()
        print("GPA: %.2f" % gpa)
        
    def __str__(self):
        return "ID: %8s, Student Name: %s" % (str(self.id), self.name)
    
    def setName(self, name):
        self.name = name

class Enrollment(persistent.Persistent):
    def __init__(self, course, grade, student):
        self.course = course
        self.grade = grade
        self.student = student

    def getCourse(self):
        return self.course
    
    def getGrade(self):
        return self.grade
    
    def printDetail(self):
        print("Course: %s, Grade: %s" % (self.course, self.grade))

    def setGrade(self, grade):
        self.grade = grade
