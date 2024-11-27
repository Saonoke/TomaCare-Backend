from fastapi import FastAPI
from routes import plant_router
from routes import auth_router
from routes import post_router
from routes import user_router
from routes import information_router
from security.middleware import RateLimitingMiddleware, AuthMiddleware

app = FastAPI()

# Add Rate Limiting Middleware
app.add_middleware(RateLimitingMiddleware)
app.add_middleware(AuthMiddleware)

# Include the auth router
app.include_router(user_router)
app.include_router(plant_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(information_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}