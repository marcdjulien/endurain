from datetime import date as date_type
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
)
from core.database import Base


class HealthSteps(Base):
    """
    SQLAlchemy model representing daily step count data for users.

    This model stores health and fitness tracking data related to the number of steps
    taken by a user on a specific date. It includes information about the data source
    and maintains a relationship with the User model.

    Attributes:
        id: Primary key, auto-incremented unique identifier.
        user_id: Foreign key referencing users.id.
        date: Calendar date for which the step count is recorded.
        steps: Total number of steps taken on the date.
        source: Source of the step data (e.g., fitness device, app).
        user: Relationship to the User model.

    Table:
        health_steps

    Relationships:
        - Many-to-One with User model through user_id
    """

    __tablename__ = "health_steps"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User ID that the health_steps belongs",
    )
    date: Mapped[date_type] = mapped_column(
        nullable=False,
        index=True,
        comment="Health steps date (date)",
    )
    steps: Mapped[int] = mapped_column(
        nullable=False,
        comment="Number of steps taken",
    )
    source: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="Source of the health steps data",
    )

    # Define a relationship to the User model
    # TODO: Change to Mapped["User"] when all modules use mapped
    user = relationship("User", back_populates="health_steps")


class HealthStepsIntraday(Base):
    """
    SQLAlchemy model representing intra-day level step count data for users.

    This model stores health and fitness tracking data related to the number of steps
    taken by a user at specific timestamps. It includes information about the data source
    and maintains a relationship with the User model.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for each record.
        user_id (int): Foreign key referencing users.id. Identifies the user who owns
            this health data. Cascades on delete and is indexed for performance.
        timestamp (datetime): The timestamp for which the step count is recorded.
        steps (int): The total number of steps taken on the specified date.
        source (str, optional): The source or origin of the step data (e.g., fitness
            device, mobile app). Maximum length of 250 characters.
        user (relationship): SQLAlchemy relationship to the User model, enabling
            bidirectional access between users and their health step records.

    Table:
        health_steps_intraday

    Relationships:
        - Many-to-One with User model through user_id
    """

    __tablename__ = "health_steps_intraday"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User ID that the health_steps belongs",
    )
    timestamp = Column(
        DateTime,
        nullable=False,
        comment="Health steps timestamp (datetime)",
    )
    steps = Column(
        Integer,
        nullable=False,
        comment="Number of steps taken",
    )
    source = Column(
        String(250),
        nullable=True,
        comment="Source of the health steps data",
    )

    # Define a relationship to the User model
    user = relationship("User", back_populates="health_steps_intraday")
