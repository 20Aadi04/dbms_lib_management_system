-- login 
Select password
from librarian
where librarian_id = { self.id_entry.get() };
-- registration
INSERT INTO Librarian (
        Librarian_ID,
        FName,
        LName,
        DOB,
        Shift,
        email,
        password
    )
VALUES (%s, %s, %s, %s, %s, %s, %s);
--Add book
INSERT INTO Book (B_Name, ISBN, Authors, Pub, Category)
VALUES (%s, %s, ARRAY [%s], %s, %s);
-- remove book 
DELETE FROM Book
WHERE B_ID = %s;
-- add seat number
SELECT get_next_available_seat('{location}');
INSERT INTO Seat (location, seat_no)
VALUES (%s, %s);
-- get next avaiable seat and update it
SELECT get_next_available_seat('{location}');
INSERT INTO Seat (location, seat_no)
VALUES (%s, %s);
-- show and remove seat 
SELECT seat_no
FROM Seat
WHERE location = %s
ORDER BY seat_no;
DELETE FROM Seat
WHERE location = %s
    AND seat_no = %s;
-- statistics
--graphs
-- preferred location graphs
SELECT location,
    COUNT(location)
FROM seat
WHERE seat_id in (
        select seat_id
        from booking
    )
GROUP BY location;
--Preferred Books
SELECT b.b_name,
    count(b.isbn),
    b.isbn
from book b,
    bookingbook_id a
WHERE b.b_id = a.book_id
GROUP BY b.isbn,
    b.b_name;
-- weekly rush graph
SELECT TO_CHAR(start_time, 'Day') weekday,
    count(*)
from booking
GROUP BY weekday
ORDER BY TO_CHAR(start_time, 'Day');