# Brug Python som base image
FROM python:3.9

# Sæt arbejdsbiblioteket i containeren
WORKDIR /app

# Kopier requirements.txt til containeren
COPY requirements.txt .

# Installer afhængighederne
RUN pip install --no-cache-dir -r requirements.txt

# Kopier resten af applikationen til containeren
COPY . .

# Eksponér porten, som Flask kører på
EXPOSE 5001

# Kommando til at køre applikationen
CMD ["python", "app.py"]
