
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "events.db"

# Create the database
def setup_database():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                event TEXT NOT NULL
            )
        """)

setup_database()

# Website design
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>College Event Registration</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2ff;
            margin: 0;
            padding: 30px 15px;
        }

        .card {
            background: white;
            max-width: 450px;
            margin: auto;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px #d0d7eb;
        }

        h1 {
            color: #244b9b;
            text-align: center;
        }

        p {
            text-align: center;
            color: #555;
        }

        label {
            font-weight: bold;
        }

        input, select, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 9px 0 16px;
            border-radius: 7px;
        }

        input, select {
            border: 1px solid #ccc;
        }

        button {
            background: #2455b5;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #173c86;
        }

        a {
            color: #2455b5;
        }
    </style>
</head>

<body>
<div class="card">
    <h1>College Event Registration</h1>
    <p>Join our upcoming college events!</p>

    {% if message %}
        <p style="color:green;font-weight:bold">{{ message }}</p>
    {% endif %}

    <form method="POST">
        <label>Full Name</label>
        <input name="name" maxlength="100"
               placeholder="Enter your name" required>

        <label>Email Address</label>
        <input name="email" type="email" maxlength="254"
               placeholder="Enter your email" required>

        <label>Select Event</label>
        <select name="event" required>
            <option value="">Choose an event</option>
            <option>Technical Fest</option>
            <option>Workshop</option>
            <option>Cultural Fest</option>
            <option>Project Exhibition</option>
        </select>

        <button type="submit">Register Now</button>
    </form>

    <p><a href="/admin">View Participants</a></p>
</div>
</body>
</html>
"""

# Home page and registration
@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        event = request.form.get("event", "")

        allowed_events = [
            "Technical Fest",
            "Workshop",
            "Cultural Fest",
            "Project Exhibition"
        ]

        if not name or not email or event not in allowed_events:
            message = "Please enter valid details."
        else:
            with sqlite3.connect(DB) as con:
                con.execute(
                    "INSERT INTO registrations (name, email, event) "
                    "VALUES (?, ?, ?)",
                    (name, email, event)
                )

            message = "Registration successful!"

    return render_template_string(HOME_PAGE, message=message)

# Participants page
@app.route("/admin")
def admin():
    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, name, email, event "
            "FROM registrations ORDER BY id DESC"
        ).fetchall()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Participants</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="font-family:Arial;padding:20px">
        <h1>Registered Participants</h1>
        <p><a href="/">Back to Registration</a></p>

        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <th>ID</th><th>Name</th>
                <th>Email</th><th>Event</th>
            </tr>
            {% for r in rows %}
            <tr>
                {% for value in r %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, rows=rows)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
