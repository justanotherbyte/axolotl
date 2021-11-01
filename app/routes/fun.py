import asyncio
from typing import Union

import aiofiles
import pyppeteer
from fastapi import APIRouter, Request, Response

fun_router = APIRouter(prefix="/fun")

@fun_router.get("/screenshot")
async def take_screenshot(request: Request, url: str, delay: Union[int, float] = 0.0):
    # TODO: validate url before passing it onto pyppeteer
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

    return Response(image, media_type="image/png")
