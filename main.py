from fastapi import FastAPI, Depends, HTTPException
from src.insert.insert_routes import insert_router


app = FastAPI()


app.include_router(insert_router, prefix='/insert')