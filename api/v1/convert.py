from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
import tempfile
import pypandoc
import base64
from fastapi.security import HTTPBearer

#pypandoc.download_pandoc()

router = APIRouter(
    prefix="/convert",
    tags=["Convert"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.post("/word-to-html", dependencies=[Depends(HTTPBearer())])
async def convert_word_to_html(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .docx file.")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        output = pypandoc.convert_file(temp_path, 'html', format='docx')
        output = output.replace('\n', '')
        encoded_output = base64.b64encode(output.encode()).decode()
    finally:
        os.remove(temp_path)

    return {"html": encoded_output}
