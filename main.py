from fastapi import FastAPI
from routes import plant_router


app = FastAPI()

# Include the auth router
# app.include_router(auth_router)
app.include_router(plant_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}