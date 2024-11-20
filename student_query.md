# **SQL Queries for the Student App Backend**

---

## **1. Login Endpoint**

### **Query: Authenticate a Student**

```sql
SELECT *
FROM student
WHERE student_id = %s;
```

 Fetches the details of a student based on their `student_id` to authenticate the user.

---

## **2. Registration Endpoint**

### **Query: Register a New Student**

```sql
INSERT INTO student (student_id, fname, lname, dob, grad_type, email, phone_num, password)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
```

Inserts a new student's details into the `student` table during registration.


---

## **3. Available Seats Endpoint**

### **Query: Fetch Available Seats**

```sql
SELECT seat_id, location, seat_no
FROM seat
WHERE seat_id NOT IN (
    SELECT seat_id
    FROM booking
    WHERE (start_time < %s AND end_time > %s)
);
```

Retrieves all available seats during a specified time range.


---

## **4. Booking Conflict Check**

### **Function: Check Booking Conflict**

```sql
CREATE OR REPLACE FUNCTION check_booking_conflict(sstudent_id INT, sstart_time TIMESTAMP, send_time TIMESTAMP)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN NOT EXISTS (
        SELECT 1
        FROM booking
        WHERE student_id = sstudent_id
        AND (start_time, end_time) OVERLAPS (sstart_time, send_time)
    );
END;
$$ LANGUAGE plpgsql;
```

Checks if a student already has a booking that overlaps with the specified time range.


---

## **5. Available Books Endpoint**

### **Query: Fetch Available Books**

```sql
SELECT DISTINCT ON (b.isbn)
    b.b_id, b.b_name, b.authors, b.isbn, b.pub, b.category
FROM book b
WHERE b.b_id NOT IN (
    SELECT bb.book_id
    FROM bookingbook_id bb
    JOIN booking bk ON bb.student_id = bk.student_id AND bb.start_time = bk.start_time
    WHERE bk.start_time < %s AND bk.end_time > %s
);
```

 Fetches all books that are available during a specified time slot.
 Filters out books that are already reserved for the given time range.

---

## **6. Create Booking Endpoint**

### **Query: Create a New Booking**

#### **Insert Booking**

```sql
INSERT INTO booking (student_id, seat_id, start_time, end_time)
VALUES (%s, %s, %s, %s);
```

Adds a new booking record for a student.

#### **Insert Associated Books**

```sql
INSERT INTO bookingbook_id (student_id, start_time, end_time, book_id)
VALUES (%s, %s, %s, %s);
```

- **Purpose**: Links books to the created booking.

---

## **7. Booking History Endpoint**

### **Query: Fetch Booking History**

```sql
SELECT
    s.seat_no, s.location, b.start_time, b.end_time,
    bo.b_name, bo.isbn, bo.authors, bo.pub AS publisher
FROM booking b
JOIN seat s ON b.seat_id = s.seat_id
LEFT JOIN bookingbook_id bb ON b.student_id = bb.student_id AND b.start_time = bb.start_time
LEFT JOIN book bo ON bb.book_id = bo.b_id
WHERE b.student_id = %s
ORDER BY b.start_time DESC;
```

 Retrieves all past bookings of a student along with seat details and associated books.
 Joins `booking`, `seat`, `book`, and `bookingbook_id` tables to fetch complete booking history.

---

## **8. Current Booking Endpoint**

### **Query: Fetch Current Booking**

```sql
SELECT s.seat_no, s.location, b.start_time, b.end_time, bo.b_name,
    bo.isbn, bo.authors, bo.pub AS publisher
FROM booking b
JOIN seat s ON b.seat_id = s.seat_id
LEFT JOIN bookingbook_id bb ON b.student_id = bb.student_id AND b.start_time = bb.start_time
LEFT JOIN book bo ON bb.book_id = bo.b_id
WHERE (b.student_id, b.start_time) IN (
        SELECT student_id, start_time
        FROM booking
        WHERE student_id = %s
        ORDER BY start_time
        LIMIT 1
    )
    AND b.end_time > NOW();
```

Fetches the most recent active booking for a student.
Finds the latest booking for the student where the booking is still active.

---
