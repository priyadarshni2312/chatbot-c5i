from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import create_all_tables
from app.routes import app as routes_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_all_tables()


app.include_router(routes_app)

app.mount('/', StaticFiles(directory='build', html=True), name='static')