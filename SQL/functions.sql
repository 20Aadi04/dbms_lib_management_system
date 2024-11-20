CREATE OR REPLACE FUNCTION check_booking_conflict(
        sstudent_id INT,
        sstart_time TIMESTAMP,
        send_time TIMESTAMP
    ) RETURNS BOOLEAN AS $$ BEGIN RETURN NOT EXISTS (
        SELECT 1
        FROM booking
        WHERE student_id = sstudent_id
            AND (start_time, end_time) overlaps (sstart_time, send_time)
    );
END;
$$ LANGUAGE plpgsql;
-- get seat count 
CREATE OR REPLACE FUNCTION get_seat_count(location_name VARCHAR) RETURNS INT AS $$ BEGIN RETURN (
        SELECT COUNT(*)
        FROM seat
        WHERE location = location_name
    );
END;
$$ LANGUAGE plpgsql;
-- get next available seat
CREATE OR REPLACE FUNCTION get_next_available_seat(location_name VARCHAR) RETURNS INT AS $$ BEGIN RETURN (
        SELECT number
        FROM (
                SELECT generate_series(
                        1,
                        (
                            SELECT get_seat_count(location_name) + 1
                        )
                    ) AS number
            ) AS series
        WHERE number NOT IN (
                SELECT seat_no
                FROM seat
                WHERE location = location_name
            )
        ORDER BY number
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql;