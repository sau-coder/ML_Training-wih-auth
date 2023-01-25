from fastapi import APIRouter
from fastapi import UploadFile
import os
from uuid import uuid4
from app.Files.model import FileData
from database.db import SessionLocal

router = APIRouter()
db = SessionLocal()

@router.post("/upload_file")
async def upload_file(file : UploadFile):
    file_name = file.filename
    file_directory = "file"
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)

    save_path = os.path.join(file_directory, file_name)
    with open(save_path, 'wb') as f:
        f.write(await file.read())

    new_file = FileData(
        file_id = uuid4()
    )

    db.add(new_file)
    db.commit()

    return {"message": f"File {file_name} saved successfully"}