import sys
import os
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv('MONGODB_URL_KEY')
print(mongo_db_url)
import pymongo
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DB_NAME
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

database = client[DATA_INGESTION_DB_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',tags='authentication')
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train',tags='training')
async def train():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response(content='Training successful', media_type='text/plain')
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

if __name__ == "__main__":
    app_run(app, host='localhost', port=8080)