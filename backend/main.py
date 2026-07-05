import os
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models.history import ProcessingHistory
from routes.image_routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Image Converter API", version="1.0.0")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

