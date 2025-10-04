"""SQLAlchemy database models for mystery party game."""

import uuid
from datetime import datetime
from typing import List
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
import enum
from src.database.base import Base


class GameStatus(str, enum.Enum):
    """Status of a game generation."""
    INITIALIZED = "initialized"
    CHARACTERS_GENERATED = "characters_generated"
    PLOT_GENERATED = "plot_generated"
    CLUES_GENERATED = "clues_generated"
    METADATA_GENERATED = "metadata_generated"
    VALIDATED = "validated"
    COMPLETED = "completed"
    FAILED = "failed"


class Game(Base):
    """Game table - stores the state of a mystery game generation."""

    __tablename__ = "games"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    theme = Column(String, nullable=False)
    num_players = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    special_requests = Column(Text, nullable=True)
    language = Column(String, nullable=False, default="en")
    status = Column(SQLEnum(GameStatus), nullable=False, default=GameStatus.INITIALIZED)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    characters = relationship("GeneratedCharacter", back_populates="game", cascade="all, delete-orphan")
    plot = relationship("GeneratedPlot", back_populates="game", uselist=False, cascade="all, delete-orphan")
    clues = relationship("GeneratedClue", back_populates="game", cascade="all, delete-orphan")
    game_metadata = relationship("GeneratedMetadata", back_populates="game", uselist=False, cascade="all, delete-orphan")
    validation_results = relationship("ValidationResult", back_populates="game", cascade="all, delete-orphan")


class GeneratedCharacter(Base):
    """GeneratedCharacter table - stores characters for a game."""

    __tablename__ = "generated_characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    background = Column(Text, nullable=False)
    personality = Column(Text, nullable=False)
    secret = Column(Text, nullable=False)
    motive = Column(Text, nullable=True)
    relationship_to_victim = Column(String, nullable=True)

    # Relationships
    game = relationship("Game", back_populates="characters")


class GeneratedPlot(Base):
    """GeneratedPlot table - stores the plot for a game."""

    __tablename__ = "generated_plots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False, unique=True)
    setting = Column(Text, nullable=False)
    victim = Column(String, nullable=False)
    crime = Column(Text, nullable=False)
    culprit = Column(String, nullable=False)
    murder_method = Column(Text, nullable=False)
    timeline = Column(JSON, nullable=False)  # List of timeline events
    resolution = Column(Text, nullable=False)

    # Relationships
    game = relationship("Game", back_populates="plot")


class GeneratedClue(Base):
    """GeneratedClue table - stores clues for a game."""

    __tablename__ = "generated_clues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    clue_id = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    revealed_by = Column(String, nullable=True)
    significance = Column(Text, nullable=False)
    misleading = Column(Boolean, nullable=False, default=False)

    # Relationships
    game = relationship("Game", back_populates="clues")


class GeneratedMetadata(Base):
    """GeneratedMetadata table - stores metadata for a game."""

    __tablename__ = "generated_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False, unique=True)
    title = Column(String, nullable=False)
    estimated_duration = Column(Integer, nullable=False)  # in minutes
    game_instructions = Column(Text, nullable=False)
    introduction = Column(Text, nullable=False)
    audio_introduction_path = Column(String, nullable=True)  # path to introduction audio file

    # Relationships
    game = relationship("Game", back_populates="game_metadata")


class ValidationResult(Base):
    """ValidationResult table - stores validation results for a game."""

    __tablename__ = "validation_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    iteration = Column(Integer, nullable=False)
    validation_passed = Column(Boolean, nullable=False)
    validation_errors = Column(JSON, nullable=True)  # List of error messages
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    game = relationship("Game", back_populates="validation_results")
