"""Audio generation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database.base import get_db
from src.services import game_service, metadata_service, audio_service


router = APIRouter(prefix="/games", tags=["audio"])


class AudioGenerationResponse(BaseModel):
    """Response for audio generation."""
    audio_introduction_url: str
    audio_instructions_url: str
    message: str


@router.post("/{game_id}/metadata/audio", response_model=AudioGenerationResponse)
async def generate_audio(game_id: str, db: Session = Depends(get_db)):
    """
    Generate audio files for introduction and instructions.

    Requires metadata to be generated first.
    Uses OpenAI TTS to convert text to speech.
    Saves audio file paths in the database.
    """
    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check metadata exists
    metadata = metadata_service.get_metadata_by_game(db, game_id)
    if not metadata:
        raise HTTPException(
            status_code=400,
            detail="Metadata must be generated first. Call POST /games/{game_id}/metadata"
        )

    # Get language from game
    language = game.language if hasattr(game, 'language') else 'en'

    try:
        # Generate audio files
        result = metadata_service.generate_audio_files(db, game_id, language)

        return AudioGenerationResponse(
            audio_introduction_url=f"/games/{game_id}/audio/introduction",
            audio_instructions_url=f"/games/{game_id}/audio/instructions",
            message="Audio files generated successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate audio: {str(e)}"
        )


@router.get("/{game_id}/audio/{audio_type}")
async def get_audio_file(game_id: str, audio_type: str, db: Session = Depends(get_db)):
    """
    Serve audio file for a game.

    Args:
        game_id: Game UUID
        audio_type: Type of audio ('introduction' or 'instructions')

    Returns:
        Audio file as MP3
    """
    # Validate audio type
    if audio_type not in ["introduction", "instructions"]:
        raise HTTPException(
            status_code=400,
            detail="audio_type must be 'introduction' or 'instructions'"
        )

    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get audio file path
    audio_path = audio_service.get_audio_file_path(game_id, audio_type)

    if not audio_path:
        raise HTTPException(
            status_code=404,
            detail=f"Audio file not found. Generate audio first with POST /games/{game_id}/metadata/audio"
        )

    # Serve the file
    return FileResponse(
        path=str(audio_path),
        media_type="audio/mpeg",
        filename=f"{game_id}_{audio_type}.mp3"
    )
