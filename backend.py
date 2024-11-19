from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize Flask app
app = Flask(__name__)

# Utility function to get database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/login', methods=['POST'])
def login():
    """Authenticate a student."""
    data = request.json
    student_id = data.get('student_id')
    password = data.get('password')

    if not student_id or not password:
        return jsonify({'error': 'Student ID and password are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Fetch student record
            cur.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
            user_data = cur.fetchone()

        if user_data:
            # Add password validation logic here if required
            return jsonify({'success': True, 'user_data': user_data})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/register', methods=['POST'])
def register():
    """Register a new student."""
    data = request.json
    required_fields = ['student_id', 'fname', 'lname', 'dob', 'grad_type', 'email', 'phone_num']

    # Validate required fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO student (student_id, fname, lname, dob, grad_type, email, phone_num)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (data['student_id'], data['fname'], data['lname'], data['dob'], data['grad_type'], data['email'], data['phone_num'])
            )
            conn.commit()
        return jsonify({'success': True, 'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()
# complex 1
@app.route('/available-seats', methods=['GET'])
def available_seats():
    """Fetch available seats for a given time range."""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({'error': 'Start time and end time are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT seat_id, location, seat_no
                FROM seat
                WHERE seat_id NOT IN (
                    SELECT seat_id
                    FROM booking
                    WHERE (start_time < %s AND end_time > %s)
                );
                """,
                (end_time, start_time)
            )
            seats = cur.fetchall()
        return jsonify({'success': True, 'seats': seats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()
""" the function 
CREATE OR REPLACE FUNCTION check_booking_conflict(sstudent_id INT, sstart_time TIMESTAMP, send_time TIMESTAMP)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN NOT EXISTS (
        SELECT 1
        FROM booking
        WHERE student_id = sstudent_id
        AND (start_time , end_time ) overlaps ( sstart_time,send_time )
    );
END;
$$ LANGUAGE plpgsql;
"""
@app.route('/check-booking-conflict', methods=['GET'])
def check_booking_conflict():
    """Check for booking conflict."""
    student_id = request.args.get('student_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not all([student_id, start_time, end_time]):
        return jsonify({'error': 'Student ID, start time, and end time are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT check_booking_conflict(%s, %s, %s);",
                (student_id, start_time, end_time)
            )
            conflict = cur.fetchone()[0]  # Result is a boolean

        if conflict:
            return jsonify({'success': True, 'conflict': False})  # No conflict
        else:
            return jsonify({'success': True, 'conflict': True})  # Conflict detected

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/available-books', methods=['GET'])
def available_books():
    """Fetch books available for a given time slot."""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({'error': 'Start time and end time are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT b.b_id, b.b_name, b.authors, b.isbn, b.pub, b.category
                FROM book b
                WHERE b.b_id NOT IN (
                    SELECT bb.book_id
                    FROM bookingbook_id bb
                    JOIN booking bk ON bb.student_id = bk.student_id AND bb.start_time = bk.start_time
                    WHERE bk.start_time < %s AND bk.end_time > %s
                );
                """,
                (end_time, start_time)
            )
            books = cur.fetchall()

        return jsonify({'success': True, 'books': books})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/create-booking', methods=['POST'])
def create_booking():
    """Create a new booking with seat and books."""
    data = request.json
    student_id = data.get('student_id')
    seat_id = data.get('seat_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    books = data.get('books', [])

    if not all([student_id, seat_id, start_time, end_time]):
        return jsonify({'error': 'Missing required booking data'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Insert booking
            cur.execute(
                """
                INSERT INTO booking (student_id, seat_id, start_time, end_time)
                VALUES (%s, %s, %s, %s)
                """,
                (student_id, seat_id, start_time, end_time)
            )

            # Insert books
            for book_id in books:
                cur.execute(
                    """
                    INSERT INTO bookingbook_id (student_id, start_time, book_id)
                    VALUES (%s, %s, %s)
                    """,
                    (student_id, start_time, book_id)
                )

            conn.commit()
        return jsonify({'success': True, 'message': 'Booking created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/booking-history', methods=['GET'])
def booking_history():
    """Fetch booking history for a student."""
    student_id = request.args.get('student_id')

    if not student_id:
        return jsonify({'error': 'Student ID is required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT 
                    s.seat_no, s.location, b.start_time, b.end_time,
                    bo.b_name AS book_name, bo.isbn, bo.authors, bo.pub AS publisher
                FROM booking b
                JOIN seat s ON b.seat_id = s.seat_id
                JOIN bookingbook_id bb ON b.student_id = bb.student_id AND b.start_time = bb.start_time
                JOIN book bo ON bb.book_id = bo.b_id
                WHERE b.student_id = %s
                ORDER BY b.start_time DESC;
                """,
                (student_id,)
            )
            bookings = cur.fetchall()

        return jsonify({'success': True, 'bookings': bookings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/current-booking', methods=['GET'])
def current_booking():
    """Fetch the current booking for a student."""
    student_id = request.args.get('student_id')

    if not student_id:
        return jsonify({'error': 'Student ID is required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Fetch the most recent active booking
            cur.execute(
                """
                SELECT 
                    s.seat_no, s.location, b.start_time, b.end_time,
                    bo.b_name AS book_name, bo.isbn, bo.authors, bo.pub AS publisher
                FROM booking b
                JOIN seat s ON b.seat_id = s.seat_id
                JOIN bookingbook_id bb ON b.student_id = bb.student_id AND b.start_time = bb.start_time
                JOIN book bo ON bb.book_id = bo.b_id
                WHERE b.student_id = %s AND b.end_time > NOW()
                ORDER BY b.start_time 
                LIMIT 1;
                """,
                (student_id,)
            )
            rows = cur.fetchall()

        if rows:
            current_booking = {
                "seat_no": rows[0]["seat_no"],
                "location": rows[0]["location"],
                "start_time": rows[0]["start_time"],
                "end_time": rows[0]["end_time"],
                "books": [
                    {
                        "book_name": row["book_name"],
                        "isbn": row["isbn"],
                        "authors": row["authors"],
                        "publisher": row["publisher"]
                    }
                    for row in rows if row["book_name"]
                ]
            }
            return jsonify({'success': True, 'current_booking': current_booking})
        else:
            return jsonify({'success': True, 'current_booking': None})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)