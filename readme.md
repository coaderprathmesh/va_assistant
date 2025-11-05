STUDENT REGISTRATION AND ADMIN VERIFICATION WEB APPLICATION

ABOUT THIS PROJECT:
This is a basic web application made using Flask.
It allows students to fill a registration form and stores their data in a sqlite database.
There is also an admin login system to verify credentials and access a chat page.

FILES INCLUDED:
python scripts:
1. app.py,  Main Python file that runs the Flask app
2. authentication.py,  Stores the admin username and password
templates/
3. registration.html,  Webpage for student registration
4. admin_verification.html,  Webpage for admin login
5. chat.html, UI for the V A smart assisstent.
static:
6. scripts.js a jawascript file responsible for operations like  sending user input to the bot's endpoint, and handling the responses recieved from the bot.
7. style.css a css file to decorate the chat bot's UI.
8. students.db,  Automatically created SQLite database for storing student data

HOW TO RUN THE APP:
1. Install Flask if not already installed:
   pip install flask

2. Run the app:
   python app.py

3. Open your browser and go to:
   http://127.0.0.1:5000/
or
 localhost:5000

HOW TO USE THE APP:
1. Student Registration:
The home page  shows a form.
   Students fill in their Name, Place, Age, Mobile, Course, Email, and Gender.
   When the form is submitted, the data is saved in students.db.

2. Admin Login:
click the link at the bottom of the registration form.
   Enter the correct admin credentials:
     Username: vision_aid_user@123
     Password: vision_aid_project@12345
if correct, V A smart assistant chat page will be rendered.
   If wrong, you will see an error message.
3. V A chat assistant:
V A smart assistant is a powerful yet simple tool to manage your records in natural language inputs! powered by Groq and  langchain with the powerful lama 3 versatile moddle.
enter your prompt in message V A assistant text box, and hit  enter.
assistant will faetch the related info from the database and render in the UI dinamically.
DATABASE INFORMATION:
The database is named students.db.
It has one table called students with the following columns:
id (auto-increment)
name
place
age
mobile\_number
course
email
gender

IMPORTANT NOTES:
The admin username and password are stored in authentication.py.

