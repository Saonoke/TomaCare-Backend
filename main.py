from fastapi import FastAPI
from routes import plant_router
from routes import auth_router
from routes import post_router

app = FastAPI()

# Include the auth router
# app.include_router(auth_router)
app.include_router(plant_router)
app.include_router(auth_router)
app.include_router(post_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}