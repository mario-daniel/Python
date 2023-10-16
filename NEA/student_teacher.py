import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

class Student:   
    def __init__(self, student_id, password, first_name, last_name, grade_class, approval = ''):
        self.student_id = student_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.grade_class = grade_class
        self.approval = approval

    def register(self):
        cursor.execute('''INSERT INTO Student (
                    student_id, 
                    password, 
                    first_name, 
                    last_name, 
                    class) VALUES (?, ?, ?, ?, ?)''', (
                     self.student_id, 
                     self.password, 
                     self.first_name, 
                     self.last_name, 
                     self.grade_class))
        conn.commit()

class Teacher:
    def __init__(self, teacher_id, password, first_name, last_name):
        self.teacher_id = teacher_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.facility = {'Classroom' : 1,
                         'Football Pitch' : 2,
                         'Basketball Pitch' : 3,
                         'Multi Purpose Hall' : 4,
                         'Swimming Pool' : 5,
                         }

    def register(self):
        #This inputs the new student's data into the database.
        cursor.execute('''INSERT INTO Teacher (
                    teacher_id, 
                    password, 
                    first_name, 
                    last_name, 
                    class) VALUES (?, ?, ?, ?, ?)''', (
                     self.teacher_id, 
                     self.password, 
                     self.first_name, 
                     self.last_name, 
                     self.facility))
        conn.commit()