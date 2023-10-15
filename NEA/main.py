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
    def __init__(self, teacher_id, password, first_name, last_name, facility,):
        self.teacher_id = teacher_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.facility = facility

    def register(self):
        #This inputs the new student's data into the database.
        cursor.execute('''INSERT INTO Student (
                    student_id, 
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

def Menu():
    choice_1 = input("Are you a teacher (t) or student (s): ")
    choice_2 = input('Would you like to register(r) or login(l): ')
    if choice_1 == 's':
        if choice_2 == 'r':
            student_id, password, first_name, last_name, grade_class = register(choice_1)
            student = Student(student_id, password, first_name, last_name, grade_class)
            student.register()
        elif choice_2 == 'l':
            student_id, password = login(choice_1)
    elif choice_2 == 't':
        if choice_2 == 'r':
            teacher_id, password, first_name, last_name, facility = register(choice_1)
            teacher = Teacher(teacher_id, password, first_name, last_name, facility)
            teacher.register()

def login(choice_1):
    if choice_1 == 's':
        student_id = int(input('Enter student ID: '))
        password = input('Enter password: ')
        cursor.execute('SELECT password FROM Student WHERE student_id = ?', (student_id))
        return student_id, password
    elif choice_1 == 't':
        teacher_id = int(input("Enter teacher ID: "))
        password = input('Enter password: ')
        return teacher_id, password

def register(choice_1):
    if choice_1 == 's':
        student_id = int(input("Enter student ID: "))
        password = input('Enter a password: ')
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        grade_class = input("Enter your grade and class: ")
        return student_id, password, first_name, last_name, grade_class
    elif choice_1 == 't':
        teacher_id = int(input("Enter teacher ID: "))
        password = input('Enter a password: ')
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        facility = input("What facility are you responsible for?: ")
        return teacher_id, password, first_name, last_name, facility

def main():
    Menu()

if __name__ == '__main__':
    main()

conn.close()
