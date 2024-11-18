CREATE OR REPLACE FUNCTION check_booking_conflict(
        sstudent_id INT,
        sstart_time TIMESTAMP,
        send_time TIMESTAMP
    ) RETURNS BOOLEAN AS $$
DECLARE conflict_count INT;
BEGIN
SELECT COUNT(*) INTO conflict_count
FROM booking
WHERE student_id = sstudent_id
    AND start_time < send_time
    AND end_time > sstart_time;
RETURN conflict_count = 0;
END;
$$ LANGUAGE plpgsql;