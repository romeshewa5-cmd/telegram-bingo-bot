from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Get the real project directory (handles "bingo bot" folder)
BASE_DIR = Path(__file__).resolve().parent
WEBAPP_FILE = BASE_DIR / "webapp" / "index.html"

@app.get("/")
def root():
    return {
        "status": "Bingo backend running",
        "webapp_path": str(WEBAPP_FILE),
        "exists": WEBAPP_FILE.exists()
    }

@app.get("/play")
def play():
    if not WEBAPP_FILE.exists():
        return {
            "error": "index.html not found",
            "expected_path": str(WEBAPP_FILE)
        }

    return FileResponse(WEBAPP_FILE)

