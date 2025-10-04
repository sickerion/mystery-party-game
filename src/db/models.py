"""SQLAlchemy database models."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Enum as SQLEnum
from src.db.base import Base
from src.models.schema import DifficultyLevel
import sys


# Use JSONB for PostgreSQL, JSON for other databases
if 'postgresql' in sys.modules:
    JSONType = JSONB
else:
    JSONType = JSON


class ScenarioModel(Base):
    """Database model for saved mystery scenarios."""

    __tablename__ = "scenarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Metadata
    title = Column(String(255), nullable=False, index=True)
    theme = Column(String(100), nullable=False, index=True)
    difficulty = Column(SQLEnum(DifficultyLevel), nullable=False, index=True)
    num_players = Column(Integer, nullable=False, index=True)
    estimated_duration = Column(Integer, nullable=True)

    # Full scenario data stored as JSON
    scenario_data = Column(JSON, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Optional: User tracking (for future multi-user support)
    user_id = Column(String(255), nullable=True, index=True)

    # Optional: Additional metadata
    tags = Column(JSON, nullable=True)  # Array of tags for categorization
    is_public = Column(Integer, default=0)  # 0 = private, 1 = public

    def __repr__(self):
        return f"<ScenarioModel(id={self.id}, title={self.title}, theme={self.theme})>"
