import sqlite3
from student_teacher import Student, Teacher

conn = sqlite3.connect('rfid')
cursor = conn.cursor() 

def login_menu():
    choice_1 = input("Are you a teacher (t) or student (s): ")
    choice_2 = input('Would you like to register(r) or login(l): ')
    if choice_1 == 's':
        if choice_2 == 'r':
            student_id, password, first_name, last_name, grade_class = register(choice_1)
            student = Student(student_id, password, first_name, last_name, grade_class)
            student.register()
        elif choice_2 == 'l':
            student_id, password = login(choice_1)
    elif choice_1 == 't':
        if choice_2 == 'r':
            teacher_id, password, first_name, last_name, facility = register(choice_1)
            teacher = Teacher(teacher_id, password, first_name, last_name, facility)
            teacher.register()

def login(choice_1):
    if choice_1 == 's':
        student_id = int(input('Enter student ID: '))
        password = input('Enter password: ')
        cursor.execute('SELECT password FROM Student WHERE student_id = ?', (student_id,))
        password_2 = cursor.fetchall()
        if password == password_2[0][0]:
            print('Yes!')
        else:
            print('No')
        return student_id, password
    elif choice_1 == 't':
        teacher_id = int(input("Enter teacher ID: "))
        password = input('Enter password: ')
        cursor.execute('SELECT password FROM Teacher WHERE teacher_id = ?', (teacher_id,))
        password_2 = cursor.fetchall()
        if password == password_2[0][0]:
            print('Yes!')
        else:
            print('No')
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
    
conn.close()