from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve WebApp
app.mount("/webapp", StaticFiles(directory="webapp", html=True), name="webapp")


@app.get("/")
def root():
    return {"status": "Bingo backend running"}
