import sqlite3

conn = sqlite3.connect("rfid")
cursor = conn.cursor()

class Student:
    def __init__(self, student_id, password, first_name, last_name, grade_class, approval = ''):
        self.student_id = student_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.grade_class = grade_class
        self.approval = approval

class Teacher:
    def __init__(self, teacher_id, password, first_name, last_name, facility,):
        self.teacher_id = teacher_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.facility = facility

def Menu():
    choice = input('Would you like to register(1) or login(2): ')
    while True:
        if choice == '1':
            student = register()
            break
        elif choice == '2':
            break
        else:
            choice = input('Please input a valid choice, (1) to register or (2) to login: ')
            continue
    return student

def register():
    student_id = int(input("Enter student ID: "))
    password = input('Enter a password: ')
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    grade_class = input("Enter your grade and class: ")
    #Create student object
    student = Student(student_id, password, first_name, last_name, grade_class)
    #Create a new record for the student on database
    cursor.execute('''INSERT INTO Student (
                    student_id, 
                    password, 
                    first_name, 
                    last_name, 
                    class) VALUES (?, ?, ?, ?, ?)''', (
                    student_id, 
                    password, 
                    first_name, 
                    last_name, 
                    grade_class))
    conn.commit()
    return student

def main():
    Menu()

if __name__ == '__main__':
    main()

conn.close()
