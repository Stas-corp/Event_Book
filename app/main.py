import logging
from contextlib import asynccontextmanager 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import root, auth, event
from app.adapters.db.init_db import init_db

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s - %(name)s  - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager 
async def lifespan(app: FastAPI):    
    try:
        init_db()
        logger.info("Database initialisation complete")
    except Exception as e:
        logger.error(f"Failed connect to database: {e}")
        raise RuntimeError("Database connection failed")
    
    yield

app = FastAPI(
    title="Event Book API",
    description="REST API for managing events and bookings",
    version="0.1.0",
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(event.router)