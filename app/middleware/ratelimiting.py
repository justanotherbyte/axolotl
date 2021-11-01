from fastapi import Request
from fastapi.responses import JSONResponse

from ..config import GLOBAL_RATELIMIT


async def update_ratelimit(request: Request, call_next):
    app = request.app
    host = request.client.host
    current_request_count = app.ratelimits.get(host, 1) # Start from 1 as this would be the first request 
    # a client would send.

    if current_request_count > GLOBAL_RATELIMIT:
        payload = {
            "message": "You have exceeded the global ratelimit.",
            "status": 429
        }
        return JSONResponse(payload, status_code=429)
    
    app.ratelimits[host] = current_request_count + 1
    return await call_next(request)