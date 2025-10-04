"""Character service for CRUD operations on GeneratedCharacter model."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import GeneratedCharacter
from src.models.schema import Character


def save_characters(db: Session, game_id: str, characters: List[Character]) -> List[GeneratedCharacter]:
    """
    Save characters for a game.

    Args:
        db: Database session
        game_id: Game UUID
        characters: List of Character objects from Pydantic

    Returns:
        List of created GeneratedCharacter objects
    """
    db_characters = []
    for char in characters:
        db_char = GeneratedCharacter(
            game_id=game_id,
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
        )
        db.add(db_char)
        db_characters.append(db_char)

    db.commit()
    for db_char in db_characters:
        db.refresh(db_char)

    return db_characters


def get_characters_by_game(db: Session, game_id: str) -> List[GeneratedCharacter]:
    """
    Get all characters for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        List of GeneratedCharacter objects
    """
    return db.query(GeneratedCharacter).filter(GeneratedCharacter.game_id == game_id).all()


def delete_characters_by_game(db: Session, game_id: str) -> int:
    """
    Delete all characters for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        Number of characters deleted
    """
    count = db.query(GeneratedCharacter).filter(GeneratedCharacter.game_id == game_id).delete()
    db.commit()
    return count
