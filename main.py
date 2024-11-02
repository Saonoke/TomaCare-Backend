from fastapi import FastAPI
from routes import auth_router, test_route
from security.middleware import RateLimitingMiddleware

app = FastAPI()

# Add Rate Limiting Middleware
app.add_middleware(RateLimitingMiddleware)

# Include the auth router
app.include_router(auth_router)

# Mount test app (for testing middleware)
app.mount('/user', test_route.user)

@app.get("/")
async def root():
    return {"message": "Welcome to TomaCare project!"}