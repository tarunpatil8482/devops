import os
import psycopg2
from psycopg2 import sql
import time

# Read environment variables
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Retry until DB is ready
for i in range(10):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Connected to PostgreSQL!")
        break
    except Exception as e:
        print("⏳ Waiting for PostgreSQL to start...", e)
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to the database after several attempts.")

cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
);
""")

# Insert a record
cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", ("Alice", "alice@example.com"))
user_id = cur.fetchone()[0]
conn.commit()

# Retrieve record
cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
record = cur.fetchone()
print("🎉 Inserted and retrieved record:", record)

cur.close()
conn.close()
