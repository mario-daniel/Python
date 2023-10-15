import sqlite3

conn = sqlite3.connect("rfid")
cursor = conn.cursor()

#Activity Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Activity (
        activity_id CHAR(1),
        activity VARCHAR(20),
        PRIMARY KEY (activity_id)
    );
''')

#Facility Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Facility (
        facility_id CHAR(1),
        activity_id CHAR(1),
        available BOOLEAN,
        PRIMARY KEY (facility_id),
        FOREIGN KEY (activity_id) REFERENCES Activity(activity_id)
    );
''')

#Teacher Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teacher (
        teacher_id INTEGER NOT NULL,
        password VARCHAR(20),
        first_name VARCHAR(15),
        last_name VARCHAR(15),
        facility_id CHAR(1),
        PRIMARY KEY (teacher_id),
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
    );
''')

#Approval Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Approval (
        approval_id CHAR(1),
        facility_id CHAR(1),
        PRIMARY KEY (approval_id),
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
    );
''')

#Student Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student (
        student_id INTEGER NOT NULL,
        password VARCHAR(20),
        first_name VARCHAR(15),
        last_name VARCHAR(15),
        class VARCHAR(3),
        approval_id CHAR(1),
        PRIMARY KEY (student_id),
        FOREIGN KEY (approval_id) REFERENCES Approval(approval_id)
    );
''')

#Booking Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Booking (
        booking_number INTEGER,
        facility_id CHAR(1),
        student_id INTEGER,
        booking_start_time DATETIME,
        booking_end_time DATETIME,
        PRIMARY KEY (booking_number),
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id)
    );
''')

conn.commit()
conn.close()