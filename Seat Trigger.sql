CREATE
OR REPLACE FUNCTION handle_seat_removal(seat_id_input INT) RETURNS VOID AS $ $ DECLARE booking RECORD;

available_seat_id INT;

BEGIN -- Process all active bookings for the given seat
FOR booking IN
SELECT
    *
FROM
    seat_bookings
WHERE
    seat_id = seat_id_input
    AND status = 'active' LOOP -- Find an alternative seat available for the same time slot
SELECT
    seat_id INTO available_seat_id
FROM
    seats
WHERE
    seat_id != seat_id_input
    AND NOT EXISTS (
        SELECT
            1
        FROM
            seat_bookings
        WHERE
            seat_id = seats.seat_id
            AND status = 'active'
            AND (start_time, end_time) OVERLAPS (booking.start_time, booking.end_time)
    )
LIMIT
    1;

IF available_seat_id IS NOT NULL THEN -- Reallocate booking to the new seat
UPDATE
    seat_bookings
SET
    seat_id = available_seat_id
WHERE
    booking_id = booking.booking_id;

ELSE -- Cancel the booking
UPDATE
    seat_bookings
SET
    status = 'cancelled'
WHERE
    booking_id = booking.booking_id;

END IF;

END LOOP;

END;

$ $ LANGUAGE plpgsql;

CREATE TRIGGER seat_removal_trigger
AFTER
    DELETE ON seats FOR EACH ROW EXECUTE FUNCTION handle_seat_removal(OLD.seat_id);