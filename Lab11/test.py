import ZODB, ZODB.FileStorage
import transaction
import persistent
import BTrees.OOBTree

# Open ZODB storage
storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

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

# Create a BTree for storing courses
if not hasattr(root, 'courses'):
    root.courses = BTrees.OOBTree.BTree()

# Add courses
root.courses[101] = Course(101, 'Computer Programming', 3)
root.courses[201] = Course(201, 'Web Programming', 4)

# Commit the changes to the database
transaction.commit()

# Function to retrieve a course
def retrive_course(course_id):
    return root.courses.get(course_id)

# Example usage: retrieve and print a course
course = retrive_course(101)
if course:
    course.printDetail()

# Close connection and database
connection.close()
db.close()
