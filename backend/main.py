# backend/main.py
from fastapi import FastAPI

# Erstelle eine Instanz der FastAPI-App
app = FastAPI()

# Definiere einen Endpunkt für die Wurzel-URL ("/")
@app.get("/")
def read_root():
    return {"Hello": "World"}