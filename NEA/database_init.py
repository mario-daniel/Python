import sqlite3

conn = sqlite3.connect("rfid")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Facility;")
cursor.execute("DROP TABLE IF EXISTS User;")
cursor.execute("DROP TABLE IF EXISTS Booking;")
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

#Booking Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Booking (
        booking_number INTEGER PRIMARY KEY AUTOINCREMENT,
        facility_id INTEGER,
        user_id VARCHAR(10),
        booking_start_time TIME,
        booking_end_time TIME,
        booking_date DATE,
        approved BOOLEAN,
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
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

conn.commit()
conn.close()
