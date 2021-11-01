import fastapi

from .routes.fun import fun_router


class CustomApplication(fastapi.FastAPI):
    ...

app = CustomApplication()

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
