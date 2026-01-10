from enum import Enum
from pydantic import BaseModel, ConfigDict, StrictInt, Field, model_validator
from datetime import date as datetime_date, datetime 


class Source(Enum):
    """
    An enumeration representing supported sources for the application.

    Members:
        GARMIN: Garmin health data source
    """

    GARMIN = "garmin"


class HealthStepsBase(BaseModel):
    """
    Base model for health steps data.

    Represents the core attributes of a user's step count record, including the user reference,
    date of the record, number of steps taken, and the source of the data.

    Attributes:
        date (datetime_date | None): Calendar date of the steps record. Optional field.
        steps (StrictInt | None): Number of steps taken. Must be a non-negative integer. Optional field.
        source (Source | None): Source of the steps data (e.g., device, API, manual entry). Optional field.

    Configuration:
        - from_attributes: Allows model to be populated from ORM objects.
        - extra: Forbids any extra fields not defined in the model.
        - validate_assignment: Validates field values when assigned after model creation.
        - use_enum_values: Uses enum values instead of enum objects in serialization.
    """

    date: datetime_date | None = Field(None, description="Calendar date of the steps")
    steps: StrictInt | None = Field(None, ge=0, description="Number of steps taken")
    source: Source | None = Field(None, description="Source of the steps data")

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )


class HealthStepsCreate(HealthStepsBase):
    """
    Pydantic model for creating health steps records.

    Automatically sets the date to today if not provided during instance creation.

    Attributes:
        Inherits all attributes from HealthStepsBase.

    Validators:
        set_default_date: Ensures that if no date is provided, it defaults to today's date.
    """

    @model_validator(mode="after")
    def set_default_date(self) -> "HealthStepsCreate":
        """Set date to today if not provided."""
        if self.date is None:
            self.date = datetime_date.today()
        return self


class HealthStepsRead(HealthStepsBase):
    """
    Schema for reading health steps records.

    Extends the base health steps schema with an identifier field for retrieving
    or referencing existing steps records in the database.

    Attributes:
        id (StrictInt): Unique identifier for the steps record to update. Required field.
        user_id (StrictInt): Foreign key reference to the user. Required field.
    """

    id: StrictInt = Field(
        ..., description="Unique identifier for the steps record to update"
    )
    user_id: StrictInt = Field(..., description="Foreign key reference to the user")


class HealthStepsUpdate(HealthStepsRead):
    """
    Schema for updating health steps records.

    Inherits from HealthStepsRead to maintain consistency with read operations
    while allowing modifications to health steps data. This schema is used for
    PUT/PATCH requests to update existing health steps entries.
    """


class HealthStepsListResponse(BaseModel):
    """
    Response model for listing health steps records.

    Attributes:
        total (StrictInt): Total number of steps records for the user.
        num_records (StrictInt | None): Number of records in this response.
        page_number (StrictInt | None): Current page number.
        records (list[HealthStepsRead]): List of health steps records.
    """

    total: StrictInt = Field(
        ..., description="Total number of steps records for the user"
    )
    num_records: StrictInt | None = Field(
        None, description="Number of records in this response"
    )
    page_number: StrictInt | None = Field(None, description="Current page number")
    records: list[HealthStepsRead] = Field(
        ..., description="List of health steps records"
    )

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
    )


class HealthStepsIntraday(BaseModel):
    """
    Pydantic model for health steps measured at intra-day granularity.

    Attributes:
        id (int | None): Unique identifier for the health steps record. Defaults to None.
        user_id (int | None): ID of the user associated with the steps record. Defaults to None.
        timestamp (datetime | None): Timestamp when the steps were recorded. Defaults to None.
        steps (int | None): Number of steps recorded. Defaults to None.
        source (Source | None): Source from which the steps data was obtained. Defaults to None.

    Configuration:
        - from_attributes: Allows creation from ORM model attributes
        - extra: Forbids extra fields not defined in the model
        - validate_assignment: Validates field values on assignment
        - use_enum_values: Uses enum values instead of enum instances
    """

    id: int | None = None
    user_id: int | None = None
    timestamp: datetime | None = None
    steps: int | None = None
    source: Source | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )


class HealthStepsIntradayListResponse(BaseModel):
    """
    Response schema for health steps list with total count.

    This class wraps a list of health steps records along with the total count,
    number of records, and page number providing a complete response for list endpoints.

    Attributes:
        total (int): Total number of steps records for the user.
        num_records (int | None): Number of records returned in this response.
        page_number (int | None): Page number of the current response.
        records (list[HealthStepsIntraday]): List of health steps measurements.

    Configuration:
        - from_attributes: Enables population from ORM models
        - extra: Forbids extra fields not defined in the schema
        - validate_assignment: Validates values on assignment
    """

    total: int
    num_records: int | None = None
    page_number: int | None = None
    records: list[HealthStepsIntraday]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
    )