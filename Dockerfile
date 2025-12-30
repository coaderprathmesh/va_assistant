# 1️⃣ Python version requirement
FROM python3.11.4

# 2️⃣ Set working directory inside container
WORKDIR app

# 3️⃣ Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# 4️⃣ Copy project files
COPY . .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Expose port (just documentation for now)
EXPOSE 80

# 7️⃣ Start Flask app
CMD [python, app.py]
