-- get current booking
SELECT s.seat_no,
    s.location,
    b.start_time,
    b.end_time,
    bo.b_name,
    bo.isbn,
    bo.authors,
    bo.pub AS publisher
FROM booking b
    JOIN seat s ON b.seat_id = s.seat_id
    LEFT JOIN bookingbook_id bb ON b.student_id = bb.student_id
    AND b.start_time = bb.start_time
    LEFT JOIN book bo ON bb.book_id = bo.b_id
WHERE (b.student_id, b.start_time) in (
        Select student_id,
            start_time
        from booking
        where student_id = 20221011
        ORDER by start_time
        limit 1
    )
    AND b.end_time > NOW();