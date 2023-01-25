from fastapi import FastAPI , APIRouter , UploadFile , File , Form , status , BackgroundTasks , Query
from typing import List
from fastapi.responses import JSONResponse
from uuid import uuid4
from database.db import SessionLocal
import pandas as pd
from app.jobs.schema import Model_types , PredictData
from sklearn.linear_model import LinearRegression , LogisticRegression
import pickle
import os
import numpy as np
from app.jobs.model import JobData
from app.User.user.model.user import User
from fastapi import HTTPException
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

db = SessionLocal()
router = APIRouter()


authorized_models = ['Linear Regression', 'Logistic Regression', 'SVM']

@router.post('/train/')
async def create_upload_file(bg_task : BackgroundTasks , file: UploadFile ,indepandant_columns: str = Form(...), depandant_column: str = Form(...), model_name : str = Form(...) , user_name : str = Form(...)):
    db_query = db.query(User).filter(User.user_name == user_name).first()
    if db_query is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Please create user first")

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid file type, expected CSV.")

    data = pd.read_csv(file.file)
    input_columns = indepandant_columns.split(',')
    output_columns = depandant_column.split(',')
    csv_columns = data.columns.tolist()

    for col in input_columns:
        if col not in csv_columns:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="please entered valid column name")
        X = data.drop(depandant_column , axis=1)
        Y = data[output_columns]

        x_train , x_test , y_train , y_test = train_test_split(X , Y , test_size=0.30 , random_state=10)
        print(x_train)
        print(y_train)

        if model_name not in authorized_models:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = "invalid model_name")
        
        try:
            global model
            if model_name == "Linear Regression":
                model = LinearRegression()

            elif model_name == "Logistic Regression":
                model = LogisticRegression(solver='lbfgs', max_iter=100)


            bg_task.add_task(model.fit(x_train , y_train))
            accuracy = accuracy_score(y_test , model.predict(x_test))

            model_id = str (uuid4())

            model_directory = "models"
            if not os.path.exists(model_directory):
                os.makedirs(model_directory)

            model_path = os.path.join(model_directory, f"{model_id}.pkl")
            pickle.dump(model , open(model_path , 'wb'))
            model_info = {"model_id" : model_id , "model_name" : model_name , "accuracy": accuracy , "info" : "model is trained and created successfully"}

            new_job = JobData(
                job_id = model_id,
                job_name = model_name,
                user_name = user_name
            )
            db.add(new_job)
            db.commit()

            return JSONResponse(content = model_info)

        except Exception as e:
            return {"status" : f"error while training: {e}"}
    

    

@router.post('/user_model/{user_name}')
def get_model(user_name : str):
    db_user = db.query(JobData).filter(JobData.user_name == user_name).all()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail= "User not found")

    return{
        "data" : db_user
    }