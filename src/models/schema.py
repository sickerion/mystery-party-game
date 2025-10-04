"""Pydantic models for mystery party game data structures."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class DifficultyLevel(str, Enum):
    """Mystery difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Character(BaseModel):
    """A character in the mystery party game."""

    name: str = Field(..., description="Character's name")
    role: str = Field(..., description="Character's role or occupation")
    background: str = Field(..., description="Character's background story")
    personality: str = Field(..., description="Character's personality traits")
    secret: str = Field(..., description="Character's hidden secret")
    motive: Optional[str] = Field(None, description="Motive if character is involved in the crime")
    relationship_to_victim: Optional[str] = Field(None, description="Relationship to the victim")


class Clue(BaseModel):
    """A clue in the mystery game."""

    clue_id: str = Field(..., description="Unique identifier for the clue")
    description: str = Field(..., description="Description of the clue")
    location: str = Field(..., description="Where the clue is found")
    revealed_by: Optional[str] = Field(None, description="Character who possesses or reveals this clue")
    significance: str = Field(..., description="Why this clue is important to solving the mystery")
    misleading: bool = Field(False, description="Whether this is a red herring")


class Plot(BaseModel):
    """The main plot and storyline of the mystery."""

    setting: str = Field(..., description="Setting of the mystery (time and place)")
    victim: str = Field(..., description="Name of the victim")
    crime: str = Field(..., description="The crime that occurred")
    culprit: str = Field(..., description="Name of the culprit")
    murder_method: str = Field(..., description="How the crime was committed")
    timeline: List[str] = Field(..., description="Timeline of events leading to and after the crime")
    resolution: str = Field(..., description="How the mystery is solved")


class MysteryScenario(BaseModel):
    """Complete mystery party game scenario."""

    title: str = Field(..., description="Title of the mystery scenario")
    theme: str = Field(..., description="Theme of the mystery (e.g., noir, mansion, cruise)")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level of the mystery")
    num_players: int = Field(..., ge=3, le=12, description="Number of players (3-12)")
    estimated_duration: int = Field(..., description="Estimated play duration in minutes")

    plot: Plot = Field(..., description="Main plot and storyline")
    characters: List[Character] = Field(..., description="List of characters in the game")
    clues: List[Clue] = Field(..., description="List of clues to be discovered")

    game_instructions: str = Field(..., description="Instructions for the game host")
    introduction: str = Field(..., description="Opening scene/introduction to set the stage")


class GameRequest(BaseModel):
    """Request to generate a mystery party game."""

    theme: str = Field(..., description="Desired theme for the mystery", examples=["film noir", "victorian mansion", "luxury cruise"])
    num_players: int = Field(..., ge=3, le=12, description="Number of players")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="Desired difficulty level")
    special_requests: Optional[str] = Field(None, description="Any special requests or constraints")
