from fastapi import FastAPI
from src.insert.insert_routes import insert_router
from src.select.select_route import get_data


app = FastAPI()


app.include_router(insert_router, prefix='/insert')
app.include_router(get_data, prefix='/company')