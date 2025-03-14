from flask import Flask, jsonify, request
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
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, content, latitude, longitude, createdat, views FROM posts order by id asc;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[3], "author": row[2], "latitude": row[4], "longitude": row[5], "createdat": row[6], "views": row[7]} for row in rows]

def create_post(post):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    query = "INSERT INTO posts (title, author, favorited, content, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"
    data = (post["title"], post["author"], post["favorited"], post["content"], post["latitude"], post["longitude"])
    cur.execute(query, data)
    inserted = cur.fetchone()
    conn.commit()
    return inserted

@app.route("/posts", methods=["GET"])
def posts():
    posts = get_posts()
    return jsonify(posts)

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    post = {
        "title": data.get("title"),
        "author": data.get("author"),
        "favorited": data.get("favorited"),
        "content": data.get("content"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude")
    }
    return jsonify(create_post(post))

if __name__ == "__main__":
    app.run(debug=True, port=4001)
