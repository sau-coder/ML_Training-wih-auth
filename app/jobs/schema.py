from fastapi import FastAPI , UploadFile , File , Form
from pydantic import BaseModel
from enum import Enum
from typing import List
class Model_types(str , Enum):
    linear_regression = "Linear Regression"
    logistic_regression = "Logistic Regression"
    rendom_forest = "Rendom Forest"

class UserInput(BaseModel):
    name_indepandant_variables : List[str] = []
    name_of_depandant_variable : str
    output_variable : int

class PredictData(BaseModel):
    model_name : Model_types = Form(...)
    user_name : str

    class config:
        orm_mode = True


    





