CREATE OR REPLACE FUNCTION handle_book_removal(book_id_input INT)
RETURNS VOID AS $$
DECLARE
    booking RECORD;
    available_copy_id INT;
BEGIN
    -- Process all active bookings for the given book
    FOR booking IN
        SELECT * 
        FROM book_bookings 
        WHERE book_id = book_id_input AND status = 'active'
    LOOP
        -- Find an alternative copy available for the same time slot
        SELECT copy_id INTO available_copy_id
        FROM books
        WHERE title = (SELECT title FROM books WHERE book_id = book_id_input)
          AND copy_id != book_id_input
          AND NOT EXISTS (
              SELECT 1 
              FROM book_bookings
              WHERE book_id = books.copy_id 
                AND status = 'active'
                AND (start_time, end_time) OVERLAPS (booking.start_time, booking.end_time)
          )
          LIMIT 1;

        IF available_copy_id IS NOT NULL THEN
            -- Reallocate booking to the new copy
            UPDATE book_bookings
            SET book_id = available_copy_id
            WHERE booking_id = booking.booking_id;
        ELSE
            -- Cancel the booking
            UPDATE book_bookings
            SET status = 'cancelled'
            WHERE booking_id = booking.booking_id;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER book_removal_trigger
AFTER DELETE ON books
FOR EACH ROW
EXECUTE FUNCTION handle_book_removal(OLD.book_id);
