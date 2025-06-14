from fastapi import FastAPI

app = FastAPI(
    title="FastURL Shortener API",
    description="A simple URL shortener API using FastAPI",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastURL Shortener API"}
