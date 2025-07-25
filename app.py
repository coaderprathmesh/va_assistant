from chat import chat_bp
from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import authentication

user = authentication.user
passkey = authentication.passkey

app = Flask(__name__)
app.register_blueprint(chat_bp)
#this is the root to serve registration form
@app.route("/")
def home():
    return render_template("registration.html")



# app route to collect user data and write into database
@app.route("/submit", methods=["post"])
def submit():
    full_name = request.form["full_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    gender = request.form["gender"]
    visual_acuity = request.form["visual_acuity"]
    city = request.form["city"]
    state = request.form["state"]
    country = request.form["country"]
    computer_access = request.form["computer_access"]
    english_knowledge = request.form["english_knowledge"]
    programming_languages = request.form["programming_languages"]
    source = request.form["source"]
    agentic_ai = request.form["agentic_ai"]
    expectations = request.form["expectations"]
    # writing data into database
    con = sqlite3.connect("webinar_registration.db")
    cursor = con.cursor()
    cursor.execute("""
        create table if not exists students (
            id integer primary key autoincrement,
            full_name text not null,
            email text not null,
            phone text not null,
            gender text not null,
            visual_acuity text not null,
            city text not null,
            state text not null,
            country text not null,
            computer_access text not null,
            english_knowledge text not null,
            programming_languages text not null,
            source text not null,
            agentic_ai text not null,
            expectations text not null
        )
    """)
    # insert data using lowercase command
    cursor.execute("""
        insert into students (
            full_name, email, phone, gender, visual_acuity,
            city, state, country, computer_access,
            english_knowledge, programming_languages, source,
            agentic_ai, expectations
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name, email, phone, gender, visual_acuity,
        city, state, country, computer_access,
        english_knowledge, programming_languages, source,
        agentic_ai, expectations
    ))
    con.commit()
    con.close()
    return f"Thank you for registering, {full_name}! Your response has been recorded successfully."


 #rendering verification page
@app.route("/verification", methods=["get"])
def verification_form():
    return render_template("admin_verification.html")

#root for user verification for   admin rights
@app.route("/verification", methods=["POST"])
def verification():
    user_id = request.form["userid"]
    password = request.form["password"]
    if user_id == user and password == passkey:
        return redirect(url_for("chat.chatPage"))
    else:
        return """
        <h2>Wrong credentials! Please provide a valid user ID and password.</h2>
        <p><a href="/verification">Try again</a></p>"""


#run the app
if __name__ == "__main__":
    app.run(debug=True)
