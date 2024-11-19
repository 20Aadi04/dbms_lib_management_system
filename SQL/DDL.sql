-- CREATE TYPE IF NOT EXISTS grad_type AS ENUM ('FIRST DEGREE', 'HIGHER DEGREE');
CREATE TABLE IF NOT EXISTS student (
    student_id INT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    grad_type grad_type NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (
        email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ),
    phone_num BIGINT NOT NULL UNIQUE CHECK (
        phone_num >= 1000000000
        AND phone_num <= 9999999999
    ),
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Book (
    B_ID SERIAL PRIMARY KEY,
    B_Name VARCHAR(255) NOT NULL,
    ISBN VARCHAR(255) NOT NULL,
    Authors VARCHAR(255) [],
    Pub VARCHAR(255) NOT NULL,
    Category VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Librarian (
    Librarian_ID INT PRIMARY KEY,
    FName VARCHAR(255) NOT NULL,
    LName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    Shift VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (
        email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ),
    password VARCHAR(255) not null,
    CONSTRAINT c1 CHECK (Shift in ('MORNING', 'EVENING'))
);
CREATE TABLE IF NOT EXISTS Seat (
    Seat_ID SERIAL PRIMARY KEY,
    Location VARCHAR(255) NOT NULL,
    Seat_No INT NOT NULL
);
CREATE TABLE IF NOT EXISTS Booking (
    Student_ID INT,
    Seat_ID INT,
    Start_Time TIMESTAMP NOT NULL,
    End_Time TIMESTAMP NOT NULL,
    PRIMARY KEY(Student_ID, Start_Time),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Seat_ID) REFERENCES Seat(Seat_ID) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS BookingBook_ID(
    Student_ID INT,
    Start_Time TIMESTAMP NOT NULL,
    End_Time TIMESTAMP NOT NULL,
    Book_id INT,
    FOREIGN KEY (Student_ID, Start_Time) REFERENCES Booking(Student_ID, Start_Time) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Book_id) REFERENCES Book(b_id) ON UPDATE CASCADE ON DELETE CASCADE
);