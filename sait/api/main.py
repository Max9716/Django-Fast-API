from fastapi import FastAPI
from .routers import items, flats

app = FastAPI()

app.include_router(items.router, prefix="/api")
app.include_router(flats.router, prefix="/api")