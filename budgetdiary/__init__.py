from fastapi import FastAPI

app = FastAPI()

from .route.General import subroute as general_route

app.include_router(
    general_route,
    prefix='/general',
    tags=['General']
)