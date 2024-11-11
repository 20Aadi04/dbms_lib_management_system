import os
import psycopg2
from dotenv import load_dotenv

# Lite
load_dotenv()

database_url = os.getenv('DATABASE_URL')
print(database_url)
conn = psycopg2.connect(database_url)

with conn.cursor() as cur:
    cur.execute("SELECT version()")
 
    # cur.execute("CREATE TYPE grad_type AS ENUM ('FIRST DEGREE', 'HIGHER DEGREE');")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Student (
        Student_ID INT PRIMARY KEY,
        FName VARCHAR(255) NOT NULL,
        LName VARCHAR(255) NOT NULL,
        DOB DATE NOT NULL,
        Grad_Type grad_type NOT NULL,
        Permitted_Book_count INT NOT NULL DEFAULT 3,
        email VARCHAR(255) NOT NULL,
        Phone_Num BIGINT NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Book (
        B_ID SERIAL PRIMARY KEY,
        B_Name VARCHAR(255) NOT NULL,
        ISBN VARCHAR(255) NOT NULL,
        Authors VARCHAR(255) [],
        Pub VARCHAR(255) NOT NULL,
        Category VARCHAR(255) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Librarian (
        Librarian_ID INT PRIMARY KEY,
        FName VARCHAR(255) NOT NULL,
        LName VARCHAR(255) NOT NULL,
        DOB DATE NOT NULL,
        Shift VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Seat (
        Seat_ID SERIAL PRIMARY KEY,
        Location VARCHAR(255) NOT NULL,
        Seat_No INT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Booking (
        Student_ID INT,
        Seat_ID INT,
        Start_Time TIMESTAMP NOT NULL,
        End_Time TIMESTAMP NOT NULL,
        Book_ids VARCHAR(255) [] NOT NULL,
        PRIMARY KEY(Student_ID,Start_Time,Seat_ID),
        FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        FOREIGN KEY (Seat_ID) REFERENCES Seat(Seat_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );
    """)

    cur.execute("SELECT * FROM STUDENT;")
    data = cur.fetchall()
    for i in data:
        print(i)

# Close the connection
conn.commit()
conn.close()