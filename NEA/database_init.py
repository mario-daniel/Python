import sqlite3

conn = sqlite3.connect("rfid")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Facility;")
cursor.execute("DROP TABLE IF EXISTS User;")
cursor.execute("DROP TABLE IF EXISTS Booking;")
cursor.execute("DROP TABLE IF EXISTS Timeslot;")
cursor.execute("DROP TABLE IF EXISTS Card;")
cursor.execute("DROP TABLE IF EXISTS Swipe;")

#Facility Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Facility (
        facility_id INTEGER,
        facility_name VARCHAR(15),
        booking_required BOOLEAN,
        PRIMARY KEY (facility_id)
    );
''')

#User Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id VARCHAR(10),
        facility_id INTEGER,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        hashed_password VARCHAR(100),
        salt VARCHAR(100),
        class_grade VARCHAR(3),
        PRIMARY KEY (user_id),
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
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id)
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

#Card Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Card (
        card_id INTEGER,
        user_id VARCHAR(10),
        PRIMARY KEY (card_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
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

cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (1, 'Football', 1))
cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (2, 'Sixth Form Room', 0))
cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (3, 'Basketball', 1))
cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (4, 'Crickt', 1))
cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (5, 'Multi-Purpose Hall', 1))
cursor.execute('INSERT INTO Facility VALUES (?, ?, ?)', (6, 'Fitness Suite', 1))

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
start_timings = ['07:40:00', '08:25:00 ', '09:10:00', '09:55:00', '10:15:00', '11:00:00', '11:45:00', '12:30:00', '13:10:00', '13:55:00']
end_timings = ['08:25:00 ', '09:10:00', '09:55:00', '10:15:00', '11:00:00', '11:45:00', '12:30:00', '13:10:00', '13:55:00', '14:40:00']
friday_start_timings = ['08:10:00', '08:55:00', '09:40:00', '10:25:00', '10:45:00']
friday_end_timings = ['08:55:00', '09:40:00', '10:25:00', '10:45:00', '11:30:00']
facility_ids = [1, 2, 3, 4, 5, 6]

for day in days:
    if day != 'Friday':
        for facility in facility_ids:
            for index in range(len(start_timings)):
                cursor.execute('INSERT INTO Timeslot (day, facility_id, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)', (day, facility, start_timings[index], end_timings[index], 0))
    else:
        for facility in facility_ids:
            for index in range(len(friday_start_timings)):
                dude = friday_start_timings[index]
                dude2 = friday_end_timings[index]
                cursor.execute('INSERT INTO Timeslot (day, facility_id, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)', (day, facility, friday_start_timings[index], friday_end_timings[index], 0))

conn.commit()
conn.close()
