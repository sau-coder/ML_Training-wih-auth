from fastapi import FastAPI
from app.jobs.route import router as glovbal_router
from app.User.views.route import (login_router , signup_router , protected_router , forgot_password_route , delete_route )
from app.Files.route import router as file_router 
import uvicorn
from fastapi_jwt_auth import AuthJWT
from app.User.user.schema.user import Settings

@AuthJWT.load_config
def get_config():
    return Settings()


app = FastAPI()

@app.get('/')
def models_info():
    return {"getting started with" : "model training"}

app.include_router(glovbal_router , prefix='/v1')
app.include_router(login_router , prefix='/v1')
app.include_router(signup_router ,prefix='/v1')
app.include_router(protected_router ,prefix='/v1')
app.include_router(forgot_password_route , prefix='/v1')
app.include_router(delete_route , prefix='/v1')
app.include_router(file_router , prefix='/v1')

