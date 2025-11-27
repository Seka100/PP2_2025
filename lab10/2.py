import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="snakegame",
    user="postgres",
    password="Serik_100"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    level INT DEFAULT 1,
    score INT DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    score INT,
    level INT,
    saved_at TIMESTAMP DEFAULT NOW()
)
""")
conn.commit()


def get_user(username):
    cur.execute("SELECT id, level, score FROM users WHERE username=%s", (username,))
    return cur.fetchone()


def create_user(username):
    cur.execute("INSERT INTO users(username) VALUES(%s) RETURNING id, level, score", (username,))
    conn.commit()
    return cur.fetchone()


def update_user_stats(user_id, level, score):
    cur.execute("UPDATE users SET level=%s, score=%s WHERE id=%s", (level, score, user_id))
    conn.commit()


def save_progress(user_id, score, level):
    cur.execute(
        "INSERT INTO user_score(user_id, score, level) VALUES(%s, %s, %s)",
        (user_id, score, level)
    )
    conn.commit()


def load_last_progress(user_id):
    cur.execute(
        "SELECT score, level FROM user_score WHERE user_id=%s ORDER BY saved_at DESC LIMIT 1",
        (user_id,)
    )
    return cur.fetchone()


def close_db():
    cur.close()
    conn.close()
