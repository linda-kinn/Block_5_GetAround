import uvicorn
from fastapi import FastAPI
import pandas as pd 
from pydantic import BaseModel
from typing import Union
import joblib
import json



# description will apear in the doc                                 ### NOTE_ : A MODIFIER ET ADAPTER EN FONCTION DE MON SCRIPT
description = """
Getaround API helps you predict rental price of a listing per day. 
Getaround is one of the world's largest marketplaces helping users car-sharing. The communities can find a cheaper alternative to car rentals. 
Getaround car sharing provides tech resources to help users starting a business and making money from their own vehicle business.
The goal of Getaround API is to serve data that help users estimate daily rental value of their car.
## Preview
Where you can: 
* `/preview` a some random rows in the historical record
## Model-Prediction
Where you can: 
* `/predict` insert your car details to receive an AI-based estimation on daily rental car price.
"""

# tags to identify different endpoints                              ### NOTE_ : Definition de l"URL /preview
tags_metadata = [
    {
        "name": "Preview",
        "description": "Preview the random cases in dataset",
    },

    {
        "name": "Model-Prediction",
        "description": "Estimate rental price based on machine learning model trained with historical data and XGBoost algorithm"
    }
]

app = FastAPI(
    title="🚗 Getaround API",
    description=description,
    version="1.0",
    contact={
        "name": "Hello, if you would like to learn more about my projects, check out my github.",
        "url": "https://github.com/linda-kinn",                               
    },
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/", tags=["Preview"])
async def random_data(rows: int= 3):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`.
    To avoid loading full dataset, row amount is limited to 20.
    """
    try:
        if rows < 21 :
            fname ="https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"
            df = pd.read_csv(fname)
            sample = df.sample(rows)
            response0= sample.to_json(orient='records')
        else:
            response0 = json.dumps({"message" : "Error! Please select a row number not more than 20."})
    except:
            response0 = json.dumps({"message" : "Error! Problem in accessing to historical data."})

                                                                ## NOTE_ : OPTIONNEL
mssg = """                                                    
    Error! """
#       PLease check your input. It should be in json format. Example input:
#     "model_key": "Volkswagen",
#     "mileage": 17500,
#     "engine_power": 190,
#     "fuel": "diesel",
#     "paint_color": "black",
#     "car_type": "sedan",
#     "private_parking_available": True,
#     "has_gps": True,
#     "has_air_conditioning": True,
#     "automatic_car": True,
#     "has_getaround_connect": True,
#     "has_speed_regulator": True,
#     "winter_tires": True
#     """

@app.post("/predict", tags=["Model-Prediction"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction for single set of input variables. Possible input values in order are:
    model_key: str
    mileage: float
    engine_power: float
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
    Endpoint will return a dictionnary like this:
    ```
    {'prediction': rental_price_per_day}
    ```
    You need to give this endpoint all columns values as a dictionnary, or a form data.
    """
    if predictionFeatures.json :  
      # Printing JSON as dictionnary for user to check variables
      #  requested_ = predictionFeatures.json()
        print(predictionFeatures)
      # if len (requested_.keys()) == 13 :  
        # Read data 
        df = pd.DataFrame(dict(predictionFeatures), index=[0])

        # Load the models from local
        prepro_getaround = 'prepro.joblib' # preprocessing model
        model_getaround  = 'model.joblib' # random forest model

        preprocess = joblib.load(prepro_getaround)
        regressor = joblib.load(model_getaround)
        
        try: 
            X_val = preprocess.transform(df.head(16))
            Y_pred = regressor.predict(X_val)
            print(Y_pred)
            # Prediction
            # Format response
            # Return the result as JSON but first we need to transform the
            response = {'Predicted rental price per day in dollars': round(Y_pred.tolist()[0],1)}
        except:
            response = json.dumps({"message" : mssg})
        return response
    else:
        msg = json.dumps({"message" : mssg})
        return msg

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 4000, debug=True, reload=True)