from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve webapp
if os.path.exists("webapp"):
    app.mount("/webapp", StaticFiles(directory="webapp", html=True), name="webapp")

@app.get("/")
def root():
    return {"status": "Bingo backend running"}

@app.get("/app")
def serve_app():
    return FileResponse("webapp/index.html")
