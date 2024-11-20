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