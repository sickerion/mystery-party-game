"""Audio generation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database.base import get_db
from src.services import game_service, metadata_service, audio_service


router = APIRouter(prefix="/games", tags=["audio"])


class AudioStatusResponse(BaseModel):
    """Response for audio status check."""
    has_audio: bool


class AudioGenerationResponse(BaseModel):
    """Response for audio generation."""
    audio_introduction_url: str
    message: str


@router.get("/{game_id}/audio/status", response_model=AudioStatusResponse)
async def check_audio_status(game_id: str, db: Session = Depends(get_db)):
    """
    Check if audio has been generated for a game.

    Returns:
        AudioStatusResponse with has_audio boolean
    """
    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    has_audio = metadata_service.has_audio(db, game_id)
    return AudioStatusResponse(has_audio=has_audio)


@router.post("/{game_id}/metadata/audio", response_model=AudioGenerationResponse)
async def generate_audio(game_id: str, db: Session = Depends(get_db)):
    """
    Generate audio file for introduction.

    Requires metadata to be generated first.
    Uses OpenAI TTS to convert text to speech.
    Saves audio file path in the database.
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
        # Generate audio file
        result = metadata_service.generate_audio_files(db, game_id, language)

        return AudioGenerationResponse(
            audio_introduction_url=f"/games/{game_id}/audio/introduction",
            message="Audio file generated successfully"
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
        audio_type: Type of audio ('introduction')

    Returns:
        Audio file as MP3
    """
    # Validate audio type
    if audio_type not in ["introduction"]:
        raise HTTPException(
            status_code=400,
            detail="audio_type must be 'introduction'"
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
