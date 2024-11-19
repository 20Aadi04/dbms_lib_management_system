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