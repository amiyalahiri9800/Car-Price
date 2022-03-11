from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
import sklearn
import numpy as np


class Features(BaseModel):
    Year: int
    Present_Price: int
    Kms_Driven: int
    Fuel_Type_Petrol: str
    Owner: int
    Seller_Type_Individual: str
    Transmission_Mannual: str





app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name ='static')

templates = Jinja2Templates(directory='templates')

model = pickle.load(open('random_forest_regressor_model.pkl', 'rb'))


@app.get('/predict', response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse('index.html', {"request":Request})
@app.get("/")
def home(feature: Features):
    feature = feature.dict()
    Fuel_Type_Diesel = 0
    Year = feature['Year']
    Present_Price = feature['Present_Price']
    Owner = feature['Owner']
    Kms_Driven = feature['Kms_Driven']
    Fuel_Type_Petrol = feature['Fuel_Type_Petrol'] 
    Seller_Type_Individual = feature['Seller_Type_Individual']
    Transmission_Mannual = feature['Transmission_Mannual']

    if(Fuel_Type_Petrol=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(Fuel_Type_Petrol=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
    Year=2020-Year
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0	
    
    if(Transmission_Mannual=='Mannual'):
        Transmission_Mannual=1
    else:
        Transmission_Mannual=0
    prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    output=round(prediction[0],2)
    if output < 0:
        return "You cannot sell this car"
    else:
        return ("You Can Sell The Car at {}".format(output))
    


    
    
