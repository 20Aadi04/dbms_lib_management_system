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
VALUES (%s, %s) ");