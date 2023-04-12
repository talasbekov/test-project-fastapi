import docx2txt
import html2text
import io
import aiohttp

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
        text = docx2txt.process(f)
        html = html2text.html2text(text)
        return html


@router.post("/convert/", response_class=HTMLResponse)
async def convert(url: str = Form(...)):
    docx_content = await download_file(url)
    html = convert_docx_to_html(docx_content)
    return html
