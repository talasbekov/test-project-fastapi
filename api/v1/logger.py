from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/logger",
    tags=["Logger"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("/download", status_code=status.HTTP_200_OK)
async def download_log():
    log_file_path = '/home/erp/sgo/erp-sgo-backend/logs01.log'  
    if not os.path.isfile(log_file_path):  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log file not found")

    return FileResponse(log_file_path, media_type='text/plain', filename="logs01.log")