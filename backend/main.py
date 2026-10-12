from fastapi import FastAPI

app = FastAPI(title="Personal Knowledge Base")

@app.get("/health")
def health():
    return {"status": "ok"}