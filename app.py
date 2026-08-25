import sys
import os

import certifi
from pymongo import database

from Network_Security.utils.ml_utils.model.estimator import NetworkModel
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging
from Network_Security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from Network_Security.utils.main_utils.utils import load_object

from Network_Security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from Network_Security.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

client= pymongo.MongoClient[DATA_INGESTION_DATABASE_NAME]
colletion = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
tamplates = Jinja2Templates(directory="./tamplates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworksecurityException(e,sys)

@app.get("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocessor = load_object("final_model/proprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred= network_model.predict(df)
        df['predicted_column']= y_pred
        print(df['predicted_column'])
        #df['predicted_column].replace(-1,0)
        #return df.to_json
        df.to_csv("prediction_output/output.csv")
        table_html=df.to_html(classes='table table-striped')
        return tamplates.TamplateResponse("table.html",{"request":request,"table":table_html})
    except Exception as e:
        raise NetworksecurityException(e,sys)

if __name__=="__name__":
    app_run(app,host="localhost",port=8000)