from database.db import base
from sqlalchemy import Column , ForeignKey , String 
from pydantic import BaseModel
from database.db import base
from app.User.user.model.user import User

class FileData(base):
    __tablename__ = "file_info"
    file_id = Column(String , primary_key = True)
    user_id = Column(String , ForeignKey(User.user_id))

