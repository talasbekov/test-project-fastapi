<<<<<<< HEAD
import os
import tempfile

import aiohttp

from fastapi import HTTPException


wkhtmltopdf_path = os.system("which wkhtmltopdf")


client_args = dict(
    trust_env=True,
    timeout=aiohttp.ClientTimeout(
        total=60,
        sock_connect=10,
        sock_read=10
    )
)


async def download_file_to_tempfile(url: str) -> str:
    try:
        async with aiohttp.ClientSession(**client_args) as session:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=404, detail="Failed to download file")
                file_content = await response.read()
                extension = url.split(".")[-1]
                with tempfile.NamedTemporaryFile(suffix=f".{extension}",
                                                 delete=False) as f:
                    f.write(file_content)
                    return f.name
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to download file with url: {url}")
=======
import os
import tempfile

import aiohttp

from fastapi import HTTPException


wkhtmltopdf_path = os.system("which wkhtmltopdf")


client_args = dict(
    trust_env=True,
    timeout=aiohttp.ClientTimeout(
        total=60,
        sock_connect=10,
        sock_read=10
    )
)


async def download_file_to_tempfile(url: str) -> str:
    try:
        async with aiohttp.ClientSession(**client_args) as session:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=404, detail="Failed to download file")
                file_content = await response.read()
                extension = url.split(".")[-1]
                with tempfile.NamedTemporaryFile(suffix=f".{extension}",
                                                 delete=False) as f:
                    f.write(file_content)
                    return f.name
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to download file with url: {url}")
>>>>>>> erda
