from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Hello, Docker Swarm!"})

@app.route("/db")
def db():
    try:
        connection = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="testdb"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        return jsonify({"connected_to": db_name[0]})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
