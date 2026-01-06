from chat import chat_bp
from upload_csv import upload_bp
from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import authentication
from datetime import datetime

user = authentication.user
passkey = authentication.passkey

app = Flask(__name__)
app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)


# Root route to serve volunteer registration form
@app.route("/")
def home():
    return render_template("registration.html")


# Route to collect volunteer data and insert into the volunteers database
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    current_place_of_residence = request.form["current_place_of_residence"]
    my_skillset = request.form["my_skillset"]

    # Auto-generated metadata
    created_at = datetime.now().isoformat()
    user_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    referrer = request.referrer

    # Connect to the real volunteers.db file
    con = sqlite3.connect("volunteers.db")
    cursor = con.cursor()

    # Ensure the table exists (optional safety)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            submission_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            current_place_of_residence TEXT,
            my_skillset TEXT,
            field_1c8f11d TEXT,
            form_name_id TEXT,
            created_at TEXT,
            user_id INTEGER,
            user_agent TEXT,
            user_ip TEXT,
            referrer TEXT
        )
    """)

    # Insert form data
    cursor.execute("""
        INSERT INTO volunteers (
            name, email, phone, current_place_of_residence, my_skillset,
            created_at, user_agent, user_ip, referrer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, email, phone, current_place_of_residence, my_skillset,
        created_at, user_agent, user_ip, referrer
    ))

    con.commit()
    con.close()

    return f"""
    <h2>Thank you, {name}!</h2>
    <p>Your volunteer registration has been received successfully. We’re grateful for your willingness to support VisionAid’s mission.</p>
    <a href='/'>Go back</a>
    """


# Admin verification routes (unchanged)
@app.route("/verification", methods=["GET"])
def verification_form():
    return render_template("admin_verification.html")


@app.route("/verification", methods=["POST"])
def verification():
    user_id = request.form["userid"]
    password = request.form["password"]
    if user_id == user and password == passkey:
        return redirect(url_for("chat.chatPage"))
    else:
        return """
        <h2>Wrong credentials! Please provide a valid user ID and password.</h2>
        <p><a href="/verification">Try again</a></p>
        """


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
