import sys
import os

import pandas as pd

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from Network_Security.utils.ml_utils.model.estimator import NetworkModel
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.pipeline.training_pipeline import TrainingPipeline
from Network_Security.utils.main_utils.utils import load_object
# -------------------------
# FastAPI application
# -------------------------

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Templates
# -------------------------
templates = Jinja2Templates(directory="tamplates")




@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.post("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworksecurityException(e,sys)

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred= network_model.predict(df)
        df['predicted_column']= y_pred
        print(df['predicted_column'])
        #df['predicted_column].replace(-1,0)
        #return df.to_json
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)
        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse("tables.html",{"request":request,"table":table_html})
    except Exception as e:
        raise NetworksecurityException(e,sys)

if __name__=="__main__":
    app_run(app,host="localhost",port=8000)
