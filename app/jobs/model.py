
from database.db import base
from sqlalchemy import Column , String , Integer , ForeignKey
from app.User.user.model.user import User
from app.Files.model import FileData


class JobData(base):
    __tablename__ = 'jobs'
    job_id = Column(String , primary_key = True)
    job_name = Column(String)
    user_name = Column(String)
    file_id = Column(String , ForeignKey(FileData.file_id))
    user_id = Column(String , ForeignKey(User.user_id))
