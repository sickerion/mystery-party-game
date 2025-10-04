"""LangGraph state definitions for mystery generation workflow."""

from typing import List, Optional, TypedDict
from src.models.schema import Character, Clue, Plot, DifficultyLevel


class MysteryGenerationState(TypedDict):
    """State object passed through the LangGraph workflow."""

    # Input parameters
    theme: str
    num_players: int
    difficulty: DifficultyLevel
    special_requests: Optional[str]
    language: str

    # Generated content
    characters: Optional[List[Character]]
    plot: Optional[Plot]
    clues: Optional[List[Clue]]

    # Metadata
    title: Optional[str]
    estimated_duration: Optional[int]
    game_instructions: Optional[str]
    introduction: Optional[str]

    # Validation
    validation_passed: bool
    validation_errors: Optional[List[str]]

    # Workflow control
    iteration_count: int
