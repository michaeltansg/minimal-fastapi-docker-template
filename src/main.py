# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, import-error
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from routes.health import health_router
from tags import Tags
from utils.logger import get_logger

logger = get_logger(__name__)


app = FastAPI(
    root_path="/api/v1",
    openapi_tags=[
        {"name": Tags.HEALTH.value, "description": "Health check"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(health_router, prefix="/health")


@app.on_event("startup")
async def startup_event():
    pass


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    """
    This exception handler is called when a HTTPException occurs.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    This exception handler is called when a request validation error occurs.
    """
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error("%s: %s", request, exc_str)
    content = {"status_code": 10422, "message": exc_str, "data": None}
    logger.error("Received request: %s", request)
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
