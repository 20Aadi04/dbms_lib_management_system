import os
import psycopg2
from dotenv import load_dotenv

# Lite
load_dotenv()

database_url = os.getenv('DATABASE_URL')
print(database_url)
conn = psycopg2.connect(database_url)

with conn.cursor() as cur:
    with open('DDL.sql','r') as file :
        s = file.read()
        cur.execute(s)

    cur.execute("SELECT * FROM STUDENT;")
    data = cur.fetchall()
    for i in data:
        print(i)

# Close the connection
conn.commit()
conn.close()