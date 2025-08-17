from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "It's working!"}
