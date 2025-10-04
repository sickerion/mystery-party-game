"""Image generation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database.base import get_db
from src.services import game_service, metadata_service, image_service, character_service


router = APIRouter(prefix="/games", tags=["images"])


class ImageGenerationResponse(BaseModel):
    """Response for image generation."""
    cover_image_url: str
    message: str


class CharacterImageGenerationResponse(BaseModel):
    """Response for character image generation."""
    character_image_url: str
    message: str


@router.post("/{game_id}/image", response_model=ImageGenerationResponse)
async def generate_cover_image(game_id: str, db: Session = Depends(get_db)):
    """
    Generate a cover image for the game.

    Only requires the game to exist (uses theme only).
    Uses DALL-E to create a themed cover image.
    Saves image path in the database.
    """
    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get language from game
    language = game.language if hasattr(game, 'language') else 'en'

    try:
        # Generate cover image
        image_path = image_service.generate_cover_image(
            game_id=game_id,
            theme=game.theme,
            language=language
        )

        # Update metadata with image path
        metadata_service.update_image_path(db, game_id, image_path)

        return ImageGenerationResponse(
            cover_image_url=f"/games/{game_id}/image",
            message="Cover image generated successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image: {str(e)}"
        )


@router.get("/{game_id}/image")
async def get_cover_image(game_id: str, db: Session = Depends(get_db)):
    """
    Serve cover image for a game.

    Args:
        game_id: Game UUID

    Returns:
        Cover image as PNG
    """
    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get image file path
    image_path = image_service.get_image_file_path(game_id)

    if not image_path:
        raise HTTPException(
            status_code=404,
            detail=f"Cover image not found. Generate image first with POST /games/{game_id}/metadata/image"
        )

    # Serve the file
    return FileResponse(
        path=str(image_path),
        media_type="image/png",
        filename=f"{game_id}_cover.png"
    )


@router.post("/{game_id}/characters/{character_id}/image", response_model=CharacterImageGenerationResponse)
async def generate_character_portrait_endpoint(
    game_id: str,
    character_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate a portrait image for a specific character.

    Requires character to be generated first.
    Uses DALL-E to create a character portrait.
    Saves image path in the database.
    """
    print(f"[CHARACTER IMAGE] Received request for game {game_id}, character {character_id}")

    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        print(f"[CHARACTER IMAGE] Game {game_id} not found")
        raise HTTPException(status_code=404, detail="Game not found")

    # Get character
    character = character_service.get_character_by_id(db, character_id)
    if not character or character.game_id != game_id:
        print(f"[CHARACTER IMAGE] Character {character_id} not found or doesn't belong to game {game_id}")
        raise HTTPException(status_code=404, detail="Character not found")

    print(f"[CHARACTER IMAGE] Generating portrait for {character.name} (theme: {game.theme})")

    # Get language from game
    language = game.language if hasattr(game, 'language') else 'en'

    try:
        # Generate character portrait
        image_path = image_service.generate_character_portrait(
            game_id=game_id,
            character_id=character_id,
            name=character.name,
            role=character.role,
            personality=character.personality,
            theme=game.theme,
            language=language
        )

        print(f"[CHARACTER IMAGE] Successfully generated portrait: {image_path}")

        # Update character with image path
        character_service.update_character_image_path(db, character_id, image_path)

        return CharacterImageGenerationResponse(
            character_image_url=f"/games/{game_id}/characters/{character_id}/image",
            message=f"Portrait generated successfully for {character.name}"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate character portrait: {str(e)}"
        )


@router.get("/{game_id}/characters/{character_id}/image")
async def get_character_portrait(
    game_id: str,
    character_id: int,
    db: Session = Depends(get_db)
):
    """
    Serve portrait image for a character.

    Args:
        game_id: Game UUID
        character_id: Character ID

    Returns:
        Character portrait image as PNG
    """
    # Check game exists
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get character
    character = character_service.get_character_by_id(db, character_id)
    if not character or character.game_id != game_id:
        raise HTTPException(status_code=404, detail="Character not found")

    # Get image file path
    image_path = image_service.get_character_image_file_path(
        game_id=game_id,
        character_id=character_id,
        character_name=character.name
    )

    if not image_path:
        raise HTTPException(
            status_code=404,
            detail=f"Character portrait not found. Generate image first with POST /games/{game_id}/characters/{character_id}/image"
        )

    # Serve the file
    return FileResponse(
        path=str(image_path),
        media_type="image/png",
        filename=f"{game_id}_character_{character_id}.png"
    )
