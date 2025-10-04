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


def get_character_by_id(db: Session, character_id: int) -> Optional[GeneratedCharacter]:
    """
    Get a character by ID.

    Args:
        db: Database session
        character_id: Character ID

    Returns:
        GeneratedCharacter object or None if not found
    """
    return db.query(GeneratedCharacter).filter(GeneratedCharacter.id == character_id).first()


def update_character_image_path(
    db: Session,
    character_id: int,
    character_image_path: str,
) -> Optional[GeneratedCharacter]:
    """
    Update character portrait image path.

    Args:
        db: Database session
        character_id: Character ID
        character_image_path: Path to the character portrait image

    Returns:
        Updated GeneratedCharacter object or None if not found
    """
    character = get_character_by_id(db, character_id)
    if not character:
        return None
    character.character_image_path = character_image_path
    db.commit()
    db.refresh(character)
    return character
