# Basis-Image verwenden
FROM python:3.11.4

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Abhängigkeiten installieren
RUN pip install flask
RUN pip install flask_login
RUN pip install flask_sqlalchemy
RUN pip install flask-bcrypt
RUN pip install flask_wtf
RUN pip install pycountry
RUN pip install Pillow==9.5.0
RUN pip install pandas


# Code in den Container kopieren
COPY . .

# Port freigeben, den die App verwendet
EXPOSE 5000

# Befehl zum Ausführen der App
CMD [ "python", "./main.py" ]
