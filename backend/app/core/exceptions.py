import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.schemas.errors import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)

_STATUS_CODE_TO_ERROR_CODE = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    500: "INTERNAL_SERVER_ERROR",
}


def _error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    body = ErrorResponse(error=ErrorDetail(code=code, message=message), request_id=request_id)
    return JSONResponse(status_code=status_code, content=body.model_dump())


# Registered against Starlette's base HTTPException (not fastapi.HTTPException,
# a subclass) because routing-level errors like "no matching route" (404) are
# raised as the base class — a handler registered only on the subclass would
# miss them and silently fall through to FastAPI's default handler.
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    code = _STATUS_CODE_TO_ERROR_CODE.get(exc.status_code, "HTTP_ERROR")
    return _error_response(request, exc.status_code, code, str(exc.detail))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _error_response(
        request, status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", str(exc.errors())
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Unhandled exception (request_id=%s)", request_id)
    message = str(exc) if settings.environment == "development" else "Internal server error."
    return _error_response(
        request, status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", message
    )
