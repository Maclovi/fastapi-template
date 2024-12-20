import logging
import time
from enum import IntEnum

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class BoundCode(IntEnum):
    INFORMATION = 199
    SUCCESSFUL = 299
    REDIRECT = 399
    CLIENT_ERROR = 499


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        end_time = f"{time.time() - start_time:.3f}s."
        client = request.client
        status_code = response.status_code
        extra = {
            "request_url": request.url,
            "request_method": request.method,
            "request_path": request.url.path,
            "request_size": int(request.headers.get("content-length", 0)),
            "request_host": f"{client.host}:{client.port}" if client else "",
            "response_status": status_code,
            "response_size": int(response.headers.get("content-length", 0)),
            "response_duration": end_time,
        }
        if status_code <= BoundCode.INFORMATION:
            logger.info("Information response", extra=extra)
        elif status_code <= BoundCode.SUCCESSFUL:
            logger.info("Success response", extra=extra)
        elif status_code <= BoundCode.REDIRECT:
            logger.info("Redirect response", extra=extra)
        elif status_code <= BoundCode.CLIENT_ERROR:
            logger.warning("Client request error", extra=extra)
        else:
            logger.error("Server response error", extra=extra)
        return response
