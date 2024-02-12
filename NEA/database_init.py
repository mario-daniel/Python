def main():    
    import sqlite3

    conn = sqlite3.connect("rfid")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Facility;")
    #cursor.execute("DROP TABLE IF EXISTS User;")
    cursor.execute("DROP TABLE IF EXISTS Booking;")
    cursor.execute("DROP TABLE IF EXISTS Timeslot;")
    cursor.execute("DROP TABLE IF EXISTS Card;")
    cursor.execute("DROP TABLE IF EXISTS Swipe;")
    cursor.execute("DROP TABLE IF EXISTS Issue;")
    cursor.execute("DROP TABLE IF EXISTS IssueRequest;")

    #Facility Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Facility (
            facility_id INTEGER,
            facility_name VARCHAR(15),
            booking_required BOOLEAN,
            PRIMARY KEY (facility_id)
        );
    ''')

    #Card Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Card (
            card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id VARCHAR(12),
            owner CHAR(1)
        );
    ''')

    #User Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id VARCHAR(10),
            card_id INTEGER,
            facility_id INTEGER,
            first_name VARCHAR(20),
            last_name VARCHAR(20),
            hashed_password VARCHAR(100),
            salt VARCHAR(100),
            class_grade VARCHAR(3),
            PRIMARY KEY (user_id),
            FOREIGN KEY (card_id) REFERENCES Card(card_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        );
    ''')

    #Timeslot Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Timeslot (
            timeslot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            day VARCHAR(9),
            facility_id INTEGER,
            start_time TIME,
            end_time TIME,
            status BOOLEAN,
            card_id INTEGER,
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
            FOREIGN KEY (card_id) REFERENCES Card(card_id)
        );
    ''')

    #Booking Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            booking_number INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER,
            user_id VARCHAR(10),
            timeslot_id INTEGER,
            booking_date DATE,
            approved BOOLEAN,
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (timeslot_id) REFERENCES User(timeslot_id)
        );
    ''')

    #Swipe Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Swipe (
            swipe_number INTEGER,
            card_id INTEGER,
            facility_id INTEGER,
            date_time DATETIME,
            access_accepted BOOLEAN,
            PRIMARY KEY (swipe_number)
            FOREIGN KEY (card_id) REFERENCES Card(card_id)
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        );
    ''')

    #Issue Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Issue (
            issue_id INTEGER,
            issue VARCHAR(30),
            other_issue BOOLEAN,
            PRIMARY KEY (issue_id)
        );
    ''')

    #Issue Request Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS IssueRequest (
            issue_number INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id VARCHAR(30),
            facility_id BOOLEAN,
            other_issue_reason VARCHAR(200),
            resolved BOOLEAN,
            FOREIGN KEY (issue_id) REFERENCES Issue(issue_id),
            FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
        );
    ''')

    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (1, 'Football', 1))
    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (2, 'Sixth Form Room', 0))
    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (3, 'Basketball', 1))
    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (4, 'Crickt', 1))
    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (5, 'Multi-Purpose Hall', 1))
    cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (6, 'Fitness Suite', 1))

    cursor.execute('INSERT INTO Issue VALUES (?, ?, ?)', (1, 'Other', 1))
    cursor.execute('INSERT INTO Issue VALUES (?, ?, ?)', (2, 'Facility Damage', 0))
    cursor.execute('INSERT INTO Issue VALUES (?, ?, ?)', (3, 'Facility Resources Empty', 0))
    cursor.execute('INSERT INTO Issue VALUES (?, ?, ?)', (4, 'Theft of Facility Equipment', 0))
    cursor.execute('INSERT INTO Issue VALUES (?, ?, ?)', (5, 'Health Hazard', 0))


    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    start_timings = ['07:40:00', '08:25:00', '09:10:00', '09:55:00', '10:15:00', '11:00:00', '11:45:00', '12:30:00', '13:10:00', '13:55:00']
    end_timings = ['08:25:00', '09:10:00', '09:55:00', '10:15:00', '11:00:00', '11:45:00', '12:30:00', '13:10:00', '13:55:00', '14:40:00']
    friday_start_timings = ['08:10:00', '08:55:00', '09:40:00', '10:25:00', '10:45:00']
    friday_end_timings = ['08:55:00', '09:40:00', '10:25:00', '10:45:00', '11:30:00']
    facility_ids = [1, 2, 3, 4, 5, 6]

    for day in days:
        if day != 'Friday':
            for facility in facility_ids:
                for index in range(len(start_timings)):
                    cursor.execute('INSERT INTO Timeslot (day, facility_id, start_time, end_time, status, card_id) VALUES (?, ?, ?, ?, ?, ?)', (day, facility, start_timings[index], end_timings[index], 0, None))
        else:
            for facility in facility_ids:
                for index in range(len(friday_start_timings)):
                    cursor.execute('INSERT INTO Timeslot (day, facility_id, start_time, end_time, status, card_id) VALUES (?, ?, ?, ?, ?, ?)', (day, facility, friday_start_timings[index], friday_end_timings[index], 0, None))

    import random
    import string
    for i in range(0, 5):
        letters = f'{string.ascii_uppercase}0123456789'
        cursor.execute('INSERT INTO Card (tag_id) VALUES (?)', (f'{random.choice(letters)}{random.choice(letters)} {random.choice(letters)}{random.choice(letters)} {random.choice(letters)}{random.choice(letters)} {random.choice(letters)}{random.choice(letters)}',))

    conn.commit()
    conn.close()
