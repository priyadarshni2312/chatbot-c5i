from fastapi import FastAPI
from app.db import create_all_tables
from app.routes import app as routes_app

app = FastAPI()

create_all_tables()

app.include_router(routes_app)
