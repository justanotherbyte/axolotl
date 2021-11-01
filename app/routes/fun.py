import os
import re
import asyncio
from typing import Union

import aiofiles
import pyppeteer
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse


url_regex = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

fun_router = APIRouter(prefix="/fun")

@fun_router.get("/screenshot")
async def take_screenshot(url: str, delay: Union[int, float] = 0.0):
    if not url_regex.match(url):
        payload = {
            "message": "Invalid 'url' in request.",
            "status": 400
        }
        return JSONResponse(payload, status_code=400)
    
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(delay)
    image = None
    await page.screenshot(
        {"path": "screenshotResult.png"}
    )
    lock = asyncio.Lock()
    await lock.acquire()
    try:
        async with aiofiles.open("screenshotResult.png", "rb") as f:
            image = await f.read()
    finally:
        lock.release()
    
    if os.path.exists("screenshotResult.png"):
        os.remove("screenshotResult.png")

    return Response(image, media_type="image/png")

@fun_router.get("/translate")
async def translate_text(request: Request, text: str):
    translator = request.app.translator
    translated = translator.translate(text)
    src = translated.src
    dest = translated.dest
    translated_text = translated.text
    pronunciation = translated.pronunciation

    payload = {
        "src": src,
        "dest": dest,
        "translated_text": translated_text,
        "pronunciation": pronunciation
    }
    
    return JSONResponse(payload)
