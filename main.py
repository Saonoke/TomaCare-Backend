from fastapi import FastAPI
from routes import auth_router

app = FastAPI()

# Include the auth router
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}