import aiohttp
import io
import mammoth

from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/cloud-converter", tags=["CloudConvert"], dependencies=[Depends(HTTPBearer())])


async def download_file(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                raise Exception(f"Error downloading file: {resp.status}")

def convert_docx_to_html(docx_content: bytes) -> str:
    with io.BytesIO(docx_content) as f:
        result = mammoth.convert_to_html(f)
        html = result.value
        return html


@router.post("/convert/", response_class=HTMLResponse)
async def convert(url: str = Form(...)):
    docx_content = await download_file(url)
    html = convert_docx_to_html(docx_content)
    return html
