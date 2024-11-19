CREATE OR REPLACE FUNCTION before_seat_removal()
RETURNS TRIGGER AS $$
BEGIN
    -- Reassign bookings tied to the seat
    UPDATE seat_bookings
    SET seat_id = (
        SELECT seat_id 
        FROM seats 
        WHERE seat_id != OLD.seat_id 
        LIMIT 1
    )
    WHERE seat_id = OLD.seat_id;

    -- Remove bookings if no replacement seat found
    DELETE FROM seat_bookings
    WHERE seat_id = OLD.seat_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_seat_deletion
BEFORE DELETE ON seats
FOR EACH ROW
EXECUTE FUNCTION before_seat_removal();
