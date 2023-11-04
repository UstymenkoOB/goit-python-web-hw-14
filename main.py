import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()

# Define the allowed origins for CORS
origins = [
    "http://localhost:3000"
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication, contacts, and users routers under the "/api" prefix
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    """
    Initialize the FastAPILimiter with a Redis connection.

    This function initializes the FastAPILimiter using a Redis connection based on the provided configuration settings.
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    """
    Retrieve a simple greeting message.

    This endpoint returns a simple "Hello World" message when accessed.
    """
    return {"message": "Hello World"}
