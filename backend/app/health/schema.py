from pydantic import BaseModel, ConfigDict
import health.health_steps.schema as health_steps_schema

class HealthResponse(BaseModel):
    steps_response: health_steps_schema.HealthStepsListResponse
    steps_intraday_response: health_steps_schema.HealthStepsIntradayListResponse