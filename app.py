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
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DB_NAME
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
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

@app.post(
    '/predict',
    tags='prediction',
    description='Predict the class of the given input data'
)    
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model = load_object('final_model/model.pkl')
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/predicted_output.csv', index=False)
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse(request, name="table.html", context={"table": table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    app_run(app, host='localhost', port=8080)