import os
import sys
import time
import shutil
from typing import List

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from modules.oop4ftp import upload2ftp
from modules.oop4ftp import getlist4ftp

router = APIRouter()

@router.get("/api4uf/get_ftp_list", tags = ["Upload File"])
async def get_ftp_list():
    """
    查詢 FTP 資料伺服器
    """
    ftplist = getlist4ftp()
    return {
        "ftp_list": ftplist,
        "time": f"{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}"
    }

@router.post("/api4uf/upload_file_to_ftp", tags = ["Upload File"])
async def upload_file_to_ftp(file: UploadFile = File(...)):
    """
    上傳資料到 FTP 資料伺服器
    """
    with open(f"static/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload2ftp(f"static/tmp/{file.filename}")
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
