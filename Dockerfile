# 1️⃣ Use official Python image (correct + stable)
FROM python:3.11-slim

# 2️⃣ Set absolute working directory
WORKDIR /app

# 3️⃣ Install system dependencies (Node.js for MCP)
RUN apt-get update \
 && apt-get install -y curl ca-certificates \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy only requirements first (better caching)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy application source code
COPY . .

# 7️⃣ Expose Flask port
EXPOSE 80

# 8️⃣ Start Flask app
CMD ["python", "app.py"]
