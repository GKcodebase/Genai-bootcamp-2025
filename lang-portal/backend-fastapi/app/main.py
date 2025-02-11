from fastapi import FastAPI
from .routers import words, groups, study_sessions, study_activities

app = FastAPI()

app.include_router(words.router)
app.include_router(groups.router)
app.include_router(study_sessions.router)
app.include_router(study_activities.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Language Learning Portal API"}
