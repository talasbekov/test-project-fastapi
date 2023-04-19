import os
import tempfile

import aiohttp
from pydantic import AnyUrl
from fastapi import HTTPException


wkhtmltopdf_path = os.system("which wkhtmltopdf")

async def download_file_to_tempfile(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=404, detail="Failed to download file")

            file_content = await response.text(encoding='utf-8')
            extension = url.split(".")[-1]

            with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
                file_name = f.name + "." + extension
                with open(file_name, 'w') as file:
                    file.write(file_content)
                return file_name
