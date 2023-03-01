from fastapi import FastAPI

app = FastAPI()

from .route.User import subroute as user_route
app.include_router(
    user_route,
    prefix='/user',
    tags=['User']
)

from .route.Saving import subroute as saving_route
app.include_router(
    saving_route,
    prefix='/saving',
    tags=['Saving']
)

from .route.Budget import subroute as budget_route
app.include_router(
    budget_route,
    prefix='/budget',
    tags=['Budget']
)

from .route.Income import subroute as income_route
app.include_router(
    income_route,
    prefix='/income',
    tags=['Income']
)

from .route.Outcome import subroute as outcome_route
app.include_router(
    outcome_route,
    prefix='/outcome',
    tags=['Outcome']
)

# from .route.Income import subroute as income_route