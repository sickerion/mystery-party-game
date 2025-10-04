"""Metadata service for CRUD operations on GeneratedMetadata model."""

from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import GeneratedMetadata


def save_metadata(
    db: Session,
    game_id: str,
    title: str,
    estimated_duration: int,
    game_instructions: str,
    introduction: str,
) -> GeneratedMetadata:
    """
    Save or update metadata for a game.

    Args:
        db: Database session
        game_id: Game UUID
        title: Title of the mystery
        estimated_duration: Duration in minutes
        game_instructions: Instructions for the host
        introduction: Opening scene/introduction

    Returns:
        Created or updated GeneratedMetadata object
    """
    # Check if metadata already exists
    existing_metadata = get_metadata_by_game(db, game_id)

    if existing_metadata:
        # Update existing metadata
        existing_metadata.title = title
        existing_metadata.estimated_duration = estimated_duration
        existing_metadata.game_instructions = game_instructions
        existing_metadata.introduction = introduction
        db.commit()
        db.refresh(existing_metadata)
        return existing_metadata
    else:
        # Create new metadata
        db_metadata = GeneratedMetadata(
            game_id=game_id,
            title=title,
            estimated_duration=estimated_duration,
            game_instructions=game_instructions,
            introduction=introduction,
        )
        db.add(db_metadata)
        db.commit()
        db.refresh(db_metadata)
        return db_metadata


def get_metadata_by_game(db: Session, game_id: str) -> Optional[GeneratedMetadata]:
    """
    Get metadata for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        GeneratedMetadata object or None if not found
    """
    return db.query(GeneratedMetadata).filter(GeneratedMetadata.game_id == game_id).first()


def delete_metadata_by_game(db: Session, game_id: str) -> bool:
    """
    Delete metadata for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        True if deleted, False if not found
    """
    metadata = get_metadata_by_game(db, game_id)
    if metadata:
        db.delete(metadata)
        db.commit()
        return True
    return False
