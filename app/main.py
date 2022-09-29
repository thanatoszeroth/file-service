import os
import sys
from fastapi import FastAPI
from fastapi import Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path = dotenv_path)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title = "CL Hsiao API",
        version = "1.0.0",
        description = "This is a very custom OpenAPI schema",
        contact = {
            "name": "CL, Hsiao",
            "url": "https://github.com/thanatoszeroth",
            "email": "thanatoszeroth@gmail.com.tw",
        },
        license_info = {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        routes = app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Main APP
app = FastAPI()
# Swagger UI Note
app.openapi = custom_openapi
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
# Static File
app.mount("/static", StaticFiles(directory = "static"), name = "static")


@app.get("/", tags = ["Index"])
async def index():
    """
    Export swagger docs to json file.   
    File : openapi.json  
    ```sh
    curl -O ServiceIP:ServicePort/openapi.json
    ```
    """
    ServiceIP = os.getenv("ServiceIP")
    ServicePort = os.getenv("ServicePort")
    return {"api_docs": f"http://{ServiceIP}:{ServicePort}/docs"}

@app.get("/readme", tags = ["Index"])
async def readme():
    """
    ```
    DKZA5MM04420X3XM57 
    ```
    """
    try:
        return {"readme": f"© 2022 CL Hsiao. All rights reserved."}
    except Exception as e:
        return {"message": f"{e}"}

@app.get("/logo", tags = ["Index"])
async def logo():
    """
    使用 Static 資料夾
    獲得個人 Logo  
    """
    return FileResponse('static/logo/Hsiao-logo-black.png')

@app.get("/get_ip", tags = ["Index"])
def get_ip(request: Request):
    """
    獲得前端 IP  
    """
    return {
        "ip": f"{request.client.host}",
        # "x-real-ip": request.header.get("x-real-ip", ""),
        # "x-forwarded-for": request.header.get("x-forwarded-for", "")}
    }

# API Routes and Modules
from routers import api4uf
app.include_router(api4uf.router)

from routers import api4ftp
app.include_router(api4ftp.router)

from routers import api4sftp
app.include_router(api4sftp.router)
