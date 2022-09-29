import os
import sys
import time
import shutil
from typing import List

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile


router = APIRouter()

@router.get("/api4uf/clear_static_tmp_file", tags = ["Upload File"])
async def clear_static_tmp_file():
    tmp_path = f"static/tmp"
    try:
        os.makedirs(tmp_path)
    except FileExistsError:
        print("Folder Exist")
    try:
        for file in os.listdir(tmp_path):
            os.remove(os.path.join(tmp_path, file))
        return {"message": "Success"}
    except Exception as e:
        return {"message": f"{e}"}

@router.post("/api4uf/check_file_size", tags = ["Upload File"])
async def check_file_size(file: bytes = File(...)):
    return {
        "message": "Success",
        "file_size_b": f"{len(file)} B",
        "file_size_kb": f"{len(file)/1024} KB",
        "file_size_mb": f"{len(file)/1024/1024} MB",
        "file_size_gb": f"{len(file)/1024/1024/1024} GB"}


@router.post("/api4uf/upload_file_static", tags = ["Upload File"])
async def upload_file_static(file: UploadFile = File(...)):
    ServiceIP = os.getenv("ServiceIP")
    ServicePort = os.getenv("ServicePort")
    try:
        os.makedirs(f"static/tmp")
    except FileExistsError:
        print("Folder Exist")

    with open(f"static/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "message": "Success",
        "file_name": file.filename,
        "FileUrl": f"http:/{ServiceIP}:{ServicePort}/static/tmp/{file.filename}"}


@router.post("/api4uf/check_multiple_file_size", tags = ["Upload File"])
async def check_multiple_file_size(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/api4uf/upload_multiple_file_static", tags = ["Upload File"])
async def upload_multiple_file_static(files: List[UploadFile] = File(...)):
    try:
        os.makedirs(f"static/tmp")
    except FileExistsError:
        print("Folder Exist")

    for file in files:
        with open(f"static/tmp/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"file_names": [file.filename for file in files]}