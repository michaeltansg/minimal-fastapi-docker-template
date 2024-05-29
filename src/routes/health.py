# pylint: disable=all
from fastapi import APIRouter, Request
from datetime import datetime, timezone
from tags import Tags
from src.types.health_check_response import HealthCheckResponse


health_router = APIRouter(tags=[Tags.HEALTH])


@health_router.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=200,
    summary="Health Check",
    description="Health check endpoint that returns the current time in milliseconds since January 1, 1970 (midnight UTC/GMT).",
)
async def get_health(request: Request) -> HealthCheckResponse:
    ms = int(
        (
            datetime.now(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
        ).total_seconds()
        * 1000
    )
    res = HealthCheckResponse(now=ms)
    return res
