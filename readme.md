AI powered tool to to fetch information about the database (sq lite)
--------------
1. steps to run:
1.1. install node js and python.
1.2. install required packages:
"pip install -r requirements.txt"
1.3. execute the script with the command: python app.py.
1.4. visit http://localhost
note: the project is by default running on port 80.
2. User interface.
2.1. Home page.
Home page is a type of form to insert data in database (volunteers form).
Fill the fields with the data and click submit.
A dialog with confermation appears to update you on the  status of submission.
2.2. admin varification.
click on admin varification link to land on the authorization page.
enter the required details to varify you as admin, and hit submit.
you'll be redirected to the chat bot page if the details matches, alerts you about the false attempt with the dialog box otherwise.
2.3. chat page.
a simple chat page inspired by chat gpt.
enter your query in the edit box, and hit enter.
Your query updates in the big headding on the top with the answer provided by (gpt 4.0) in a standered peragraph below.
You can view the history of the chat by clicking on chat history button.
in addition to this, a special option is provided  to insert or update the data via csv file if it matches the coloumns of the db.
3. file structure:
static-
3.1.1. js files:
"scripts.js"
to handle the comunication in between client - server.
3.1.2. css file:
to give the application consistent yet stylish look.
3.1.3. audio file:
"AI_replied.mp3"
Plays when response has recieved from the server.
3.2. templates-
3.2.1. "registration.html"
Home page of the application to insert the data with a standered html form.
3.2.2. "admin_verification.html"
Page to varify as admin.
3.2.3. "chat.html"
User interface for the chat bot.
3.3. other files:
app.py
handles the operation related to insertion of data to database.
authentication.py
standered python file stored the info regarding admin varification.
chat.py
handles the comunication in between chat page and server endpoint, comunicates back and forth from frunthand to gpt API.
upload_csv.py
Handles the operation to update the data with csv file.
flask_server.bat
a simple batch file to automate launching process for the application.
note:
the path for the app.py file has to be configgered before it's use.
readme.md
Contain information about the project.
requirements.txt
used to install the required packages for the application to setup.
volunteers.db
a standered sq lite database to store the data for the project.
