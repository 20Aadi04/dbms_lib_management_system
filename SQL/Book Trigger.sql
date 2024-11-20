CREATE OR REPLACE FUNCTION book_deletion_trigger() RETURNS TRIGGER AS $$ BEGIN
UPDATE BookingBook_ID bb
SET book_id = (
        SELECT b.b_id
        FROM Book b
        WHERE b.b_id != OLD.b_id
            AND NOT EXISTS (
                SELECT 1
                FROM BookingBook_ID bb2
                WHERE bb2.book_id = b.b_id
                    AND bb2.start_time < bb.end_time
                    AND bb2.end_time > bb.start_time
            )
            and b.isbn = OLD.isbn
        LIMIT 1
    )
WHERE bb.book_id = OLD.b_id
    and EXISTS(
        SELECT b.b_id
        FROM Book b
        WHERE b.b_id != OLD.b_id
            AND NOT EXISTS (
                SELECT 1
                FROM BookingBook_ID bb2
                WHERE bb2.book_id = b.b_id
                    AND bb2.start_time < bb.end_time
                    AND bb2.end_time > bb.start_time
            )
            and b.isbn = OLD.isbn
        LIMIT 1
    );
DELETE FROM BookingBook_ID
WHERE book_id = OLD.b_id;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER before_book_deletion BEFORE DELETE ON Book FOR EACH ROW EXECUTE FUNCTION book_deletion_trigger();