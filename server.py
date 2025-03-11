from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    "dbname": "cs361-project",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432
}

def get_posts():
    """Fetch posts from the database."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, content FROM posts;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[3], "author": row[2]} for row in rows]

@app.route("/posts", methods=["GET"])
def posts():
    return jsonify(get_posts())

if __name__ == "__main__":
    app.run(debug=True, port=4001)
