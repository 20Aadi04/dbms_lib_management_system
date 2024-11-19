# library seat management system

# todo

triggers/functions/procedure ideas;

triggers:

- when a chair is removed reassign or cancel the seats;
- when a book is removed reassign or cancel the books;

4 complex queries in librarian app

Function:
insert student values check email like '%@hyderabad.bits-pilani.ac.in' under a procedure.

## complex queries

1. ~~chairs during certain time~~
2. ~~books that are free during certain time ~~
3. statistics -> at each time 1hr how many seats are occupied
4. statistics -> at each time %age of rooms occupied

Trigger for displaying 1 seat is left in that location when all seats are removed;

# completed stuff

## complex query

1. `@app.route('/available-seats', methods=['GET'])`

```sql
SELECT seat_id, location, seat_no
FROM seat
WHERE seat_id NOT IN (
	SELECT seat_id
	FROM booking
	WHERE (start_time < %s AND end_time > %s)
	);
```

2. `@app.route('/available-books', methods=['GET'])`

```sql
SELECT b.b_id, b.b_name, b.authors, b.isbn, b.pub, b.category
FROM book b
WHERE b.b_id NOT IN (
SELECT bb.book_id
FROM bookingbook_id bb
JOIN booking bk ON bb.student_id = bk.student_id AND bb.start_time = bk.start_time
WHERE bk.start_time < %s AND bk.end_time > %s
);
```

3. `@app.route('/booking-history', methods=['GET'])`

```sql
SELECT
s.seat_no, s.location, b.start_time, b.end_time,
bo.b_name AS book_name, bo.isbn, bo.authors, bo.pub AS publisher
FROM booking b
JOIN seat s ON b.seat_id = s.seat_id
JOIN bookingbook_id bb ON b.student_id = bb.student_id AND b.start_time = bb.start_time
JOIN book bo ON bb.book_id = bo.b_id
WHERE b.student_id = %s
ORDER BY b.start_time DESC;
```

4.  `@app.route('/current-booking', methods=['GET'])`

```sql
SELECT s.seat_no,
    s.location,
    b.start_time,
    b.end_time,
    bo.b_name,
    bo.isbn,
    bo.authors,
    bo.pub AS publisher
FROM booking b
    JOIN seat s ON b.seat_id = s.seat_id
    LEFT JOIN bookingbook_id bb ON b.student_id = bb.student_id
    AND b.start_time = bb.start_time
    LEFT JOIN book bo ON bb.book_id = bo.b_id
WHERE (b.student_id, b.start_time) in (
        Select student_id,
            start_time
        from booking
        where student_id = 20221011
        ORDER by start_time
        limit 1
    )
    AND b.end_time > NOW();
```

## function

1. `@app.route('/check-booking-conflict', methods=['GET'])`

```sql
CREATE OR REPLACE FUNCTION check_booking_conflict(sstudent_id INT, sstart_time TIMESTAMP, send_time TIMESTAMP)
RETURNS BOOLEAN AS $$
BEGIN
	RETURN NOT EXISTS (
	SELECT 1
	FROM booking
	WHERE student_id = sstudent_id
	AND (start_time , end_time ) overlaps ( sstart_time,send_time ));
END;
$$ LANGUAGE plpgsql;
```

## trigger

1. removal of seat may result in booking with that seat replaced with other seat that is free during the time where the replacing seat is free .

```sql
CREATE OR REPLACE FUNCTION seat_deletion_trigger() RETURNS TRIGGER AS $$ BEGIN
UPDATE booking bo
SET seat_id = (
        SELECT se.seat_id
        FROM seat se
        WHERE se.seat_id != OLD.seat_id
            AND NOT EXISTS (
                SELECT b.seat_id
                FROM booking b
                WHERE b.seat_id = se.seat_id
                    AND b.start_time < bo.end_time
                    AND b.end_time > bo.start_time
            )
        LIMIT 1
    )
WHERE bo.seat_id = OLD.seat_id;
DELETE FROM booking
WHERE seat_id = OLD.seat_id;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE or REPLACE TRIGGER before_seat_deletion BEFORE DELETE ON seat FOR EACH ROW EXECUTE FUNCTION seat_deletion_trigger();
```
