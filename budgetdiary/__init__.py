from fastapi import FastAPI

app = FastAPI()

from .route.User import subroute as user_route
# from .route.Income import subroute as income_route

app.include_router(
    user_route,
    prefix='/user',
    tags=['User']
)