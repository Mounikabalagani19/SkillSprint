from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .api.v1 import api

# This line creates the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillSprint API",
    description="API for the SkillSprint micro-learning application.",
    version="0.1.0"
)

# --- CORS MIDDLEWARE CONFIGURATION ---
# This is the crucial part that needs to be updated.
# It tells the backend to accept requests from your frontend.
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    # You can add other origins here if needed, e.g., your deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Include the main API router
app.include_router(api.api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the SkillSprint API!"}

