CREATE OR REPLACE FUNCTION book_deletion_trigger() RETURNS TRIGGER AS $$ BEGIN
UPDATE bookingbook_id
SET book_id = (
        SELECT book_id
        FROM book
        WHERE book.b_id = OLD.book_id
        LIMIT 1
    )
WHERE book_id = OLD.book_id
    AND NOT EXISTS (
        SELECT 1
        FROM bookingbook_id bb
        WHERE bb.book_id = book.b_id
            AND bb.start_time < OLD.end_time
            AND bb.end_time > OLD.start_time
    );
DELETE FROM bookingbook_id
WHERE book_id = OLD.book_id;
DELETE FROM book
WHERE b_id = OLD.book_id;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER before_book_deletion BEFORE DELETE ON book FOR EACH ROW EXECUTE FUNCTION book_deletion_trigger();