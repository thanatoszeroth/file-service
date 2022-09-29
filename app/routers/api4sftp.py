import os
import sys
import time
import shutil
from typing import List

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from modules.oop4sftp import upload2sftp
from modules.oop4sftp import getlist4sftp

router = APIRouter()

@router.get("/api4uf/get_sftp_list", tags = ["Upload File"])
async def get_sftp_list():
    """
    查詢 SFTP 資料伺服器
    """
    sftplist = getlist4sftp()
    return {
        "ftp_list": sftplist,
        "time": f"{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}"
    }

@router.post("/api4uf/upload_file_to_sftp", tags = ["Upload File"])
async def upload_file_to_sftp(file: UploadFile = File(...)):
    """
    上傳資料到 SFTP 資料伺服器
    """
    with open(f"static/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload2sftp(f"static/tmp/{file.filename}")
    try:
        os.remove(f"static/tmp/{file.filename}")
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")
    return {
        "message": "Success",
        "filename": file.filename,
        "time": f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())}"
        }
