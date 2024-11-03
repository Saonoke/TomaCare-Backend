from fastapi import FastAPI
from routes import auth_router
# from routes import user_router
from security.middleware import RateLimitingMiddleware, AuthMiddleware

app = FastAPI()

# Add Rate Limiting Middleware
app.add_middleware(RateLimitingMiddleware)
app.add_middleware(AuthMiddleware)

# Include the auth router
app.include_router(auth_router)
# Include the user router
# app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}