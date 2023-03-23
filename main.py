from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes.search import search

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(search)

uvicorn.run(app,host='0.0.0.0',port=8000)