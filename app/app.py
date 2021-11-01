import fastapi

from cachetools import TTLCache
from googletrans import Translator
from starlette.middleware.base import BaseHTTPMiddleware

from .routes.fun import fun_router
from .middleware.ratelimiting import update_ratelimit


class CustomApplication(fastapi.FastAPI):
    ratelimits: TTLCache
    translator: Translator

app = CustomApplication()
app.ratelimits = TTLCache(maxsize=float("inf"), ttl=60)
app.translator = Translator()

app.add_middleware(BaseHTTPMiddleware, dispatch=update_ratelimit)

routers = [
    fun_router
]

for router in routers:
    app.include_router(router)

@app.get("/")
async def index():
    return {
        "message": "uwu!"
    }
