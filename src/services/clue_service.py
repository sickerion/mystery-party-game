"""Clue service for CRUD operations on GeneratedClue model."""

from typing import List
from sqlalchemy.orm import Session
from src.database.models import GeneratedClue
from src.models.schema import Clue


def save_clues(db: Session, game_id: str, clues: List[Clue]) -> List[GeneratedClue]:
    """
    Save clues for a game.

    Args:
        db: Database session
        game_id: Game UUID
        clues: List of Clue objects from Pydantic

    Returns:
        List of created GeneratedClue objects
    """
    db_clues = []
    for clue in clues:
        db_clue = GeneratedClue(
            game_id=game_id,
            clue_id=clue.clue_id,
            description=clue.description,
            location=clue.location,
            revealed_by=clue.revealed_by,
            significance=clue.significance,
            misleading=clue.misleading,
        )
        db.add(db_clue)
        db_clues.append(db_clue)

    db.commit()
    for db_clue in db_clues:
        db.refresh(db_clue)

    return db_clues


def get_clues_by_game(db: Session, game_id: str) -> List[GeneratedClue]:
    """
    Get all clues for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        List of GeneratedClue objects
    """
    return db.query(GeneratedClue).filter(GeneratedClue.game_id == game_id).all()


def delete_clues_by_game(db: Session, game_id: str) -> int:
    """
    Delete all clues for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        Number of clues deleted
    """
    count = db.query(GeneratedClue).filter(GeneratedClue.game_id == game_id).delete()
    db.commit()
    return count
