"""Metadata service for CRUD operations on GeneratedMetadata model."""

from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import GeneratedMetadata
from src.services import audio_service


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


def update_audio_paths(
    db: Session,
    game_id: str,
    audio_introduction_path: Optional[str] = None,
    audio_instructions_path: Optional[str] = None,
) -> Optional[GeneratedMetadata]:
    """
    Update audio file paths in metadata.

    Args:
        db: Database session
        game_id: Game UUID
        audio_introduction_path: Path to introduction audio file
        audio_instructions_path: Path to instructions audio file

    Returns:
        Updated GeneratedMetadata object or None if not found
    """
    metadata = get_metadata_by_game(db, game_id)
    if not metadata:
        return None

    if audio_introduction_path is not None:
        metadata.audio_introduction_path = audio_introduction_path
    if audio_instructions_path is not None:
        metadata.audio_instructions_path = audio_instructions_path

    db.commit()
    db.refresh(metadata)
    return metadata


def generate_audio_files(db: Session, game_id: str, language: str = "en") -> dict:
    """
    Generate audio files for introduction and instructions.

    Args:
        db: Database session
        game_id: Game UUID
        language: Language code for TTS (en or fr)

    Returns:
        Dictionary with generated file paths

    Raises:
        ValueError: If metadata not found or OpenAI API key not configured
        Exception: If audio generation fails
    """
    # Get metadata
    metadata = get_metadata_by_game(db, game_id)
    if not metadata:
        raise ValueError(f"Metadata not found for game {game_id}")

    # Generate introduction audio
    intro_path = audio_service.generate_audio(
        text=metadata.introduction,
        game_id=game_id,
        audio_type="introduction",
        language=language
    )

    # Generate instructions audio
    instructions_path = audio_service.generate_audio(
        text=metadata.game_instructions,
        game_id=game_id,
        audio_type="instructions",
        language=language
    )

    # Update metadata with audio paths
    update_audio_paths(
        db,
        game_id,
        audio_introduction_path=intro_path,
        audio_instructions_path=instructions_path
    )

    return {
        "audio_introduction_path": intro_path,
        "audio_instructions_path": instructions_path
    }
