CREATE
OR REPLACE FUNCTION count_seats_at_location(location_name VARCHAR) RETURNS INTEGER AS $ $ DECLARE seat_count INTEGER;

BEGIN -- Count the number of seats at the specified location
SELECT
    COUNT(*) INTO seat_count
FROM
    Seat
WHERE
    location = location_name;

-- Return the count
RETURN seat_count;

END;