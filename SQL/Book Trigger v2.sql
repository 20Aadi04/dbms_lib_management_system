CREATE OR REPLACE FUNCTION before_book_removal() RETURNS TRIGGER AS $$ BEGIN -- Reassign bookings tied to the book
UPDATE book_bookings
SET book_id = (
        SELECT copy_id
        FROM books
        WHERE copy_id != OLD.book_id
            AND EXISTS (
                SELECT 1
                FROM books AS b
                WHERE b.copy_id = copy_id
                    AND b.title = OLD.title
            )
        LIMIT 1
    )
WHERE book_id = OLD.book_id;
-- Remove bookings if no replacement copy found
DELETE FROM book_bookings
WHERE book_id = OLD.book_id;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER before_book_deletion BEFORE DELETE ON books FOR EACH ROW EXECUTE FUNCTION before_book_removal();