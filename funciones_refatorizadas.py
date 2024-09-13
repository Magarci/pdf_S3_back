
#funcion de Llama3.1

def upload_pdf(db: Session, file: UploadFile, file_name: str) -> models.PDF:
    s3_client = Settings.get_s3_client()
    BUCKET_NAME = Settings().AWS_S3_BUCKET

    try:
        file_url = _upload_to_s3(s3_client, file_name)
        
        db_pdf = models.PDF(name=file.filename, selected=False, file=file_url)
        return _save_pdf(db, db_pdf)
    
    except NoCredentialsError as e:
        raise HTTPException(status_code=500, detail="Error in AWS credentials") from e


#funcion de claude3.5

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from botocore.exceptions import NoCredentialsError

from . import models
from .config import Settings

def upload_pdf(db: Session, file: UploadFile, file_name: str):
    s3_client = Settings.get_s3_client()
    bucket_name = Settings().AWS_S3_BUCKET
    
    try:
        file_url = upload_to_s3(s3_client, file, bucket_name, file_name)
        return create_pdf_record(db, file, file_url)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Error in AWS credentials")

def upload_to_s3(s3_client, file: UploadFile, bucket_name: str, file_name: str) -> str:
    s3_client.upload_fileobj(file.file, bucket_name, file_name)
    return f'https://{bucket_name}.s3.amazonaws.com/{file_name}'

def create_pdf_record(db: Session, file: UploadFile, file_url: str) -> models.PDF:
    db_pdf = models.PDF(name=file.filename, selected=False, file=file_url)
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf
