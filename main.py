from fastapi import FastAPI
from routes import auth_router
from database import engine, Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the user router
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}