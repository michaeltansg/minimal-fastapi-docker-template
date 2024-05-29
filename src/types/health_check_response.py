# pylint: disable=all
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    now: int = Field(
        description="The Unix epoch is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT).",
    )
