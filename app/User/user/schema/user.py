from pydantic import BaseModel
from dotenv import load_dotenv
import os
import phonenumbers

load_dotenv()


class UserLoginData(BaseModel):
    username: str
    password: str

    class config:
        orm_mode = True


class UserSignupData(BaseModel):
    first_name: str
    last_name: str
    username: str
    email_id: str
    mobile_no: str
    password: str
    retype_password: str

    class Config:
        orm_mode = True


class ResetPasswordData(BaseModel):
    username: str

    class config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key : str = "4efe077c4762dd8d7349cf7db10325af069e020ee52de560c0af9d3ba0579d56"
    
def mobile_no_varification(mobile_number):
    phone_number = phonenumbers.parse(mobile_number)
    valid = phonenumbers.is_valid_number(phone_number)
    return valid