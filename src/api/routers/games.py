"""Games API router - incremental game generation endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models import GameStatus
from src.models.schema import GameRequest, MysteryScenario, Character, Plot, Clue
from src.services import (
    game_service,
    character_service,
    plot_service,
    clue_service,
    metadata_service,
    validation_service,
)

router = APIRouter(prefix="/games", tags=["games"])


# Response models
from pydantic import BaseModel


class GameResponse(BaseModel):
    """Response for game creation/retrieval."""
    id: str
    theme: str
    num_players: int
    difficulty: str
    special_requests: Optional[str]
    language: str
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class GameListResponse(BaseModel):
    """Response for game listing."""
    id: str
    theme: str
    num_players: int
    difficulty: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("", response_model=GameResponse, status_code=201)
async def create_game(request: GameRequest, db: Session = Depends(get_db)):
    """
    Create a new game with initial parameters.

    The game is created in INITIALIZED status.
    """
    game = game_service.create_game(
        db=db,
        theme=request.theme,
        num_players=request.num_players,
        difficulty=request.difficulty,
        special_requests=request.special_requests,
        language=request.language,
    )

    return GameResponse(
        id=game.id,
        theme=game.theme,
        num_players=game.num_players,
        difficulty=game.difficulty,
        special_requests=game.special_requests,
        language=game.language,
        status=game.status.value,
        created_at=game.created_at.isoformat(),
        updated_at=game.updated_at.isoformat(),
    )


@router.get("", response_model=List[GameListResponse])
async def list_games(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """
    List all games with optional filtering.

    Query parameters:
    - status: Filter by game status (optional)
    - limit: Maximum number of results (default: 100)
    - offset: Number of results to skip (default: 0)
    """
    status_enum = None
    if status:
        try:
            status_enum = GameStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {status}. Valid values: {[s.value for s in GameStatus]}",
            )

    games = game_service.list_games(db, status=status_enum, limit=limit, offset=offset)

    return [
        GameListResponse(
            id=game.id,
            theme=game.theme,
            num_players=game.num_players,
            difficulty=game.difficulty,
            status=game.status.value,
            created_at=game.created_at.isoformat(),
        )
        for game in games
    ]


@router.get("/{game_id}", response_model=MysteryScenario)
async def get_game(game_id: str, db: Session = Depends(get_db)):
    """
    Get complete game scenario with all generated data.

    Returns the full MysteryScenario if all components have been generated.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get all components
    db_characters = character_service.get_characters_by_game(db, game_id)
    db_plot = plot_service.get_plot_by_game(db, game_id)
    db_clues = clue_service.get_clues_by_game(db, game_id)
    db_metadata = metadata_service.get_metadata_by_game(db, game_id)

    # Check if all components exist
    if not db_characters:
        raise HTTPException(
            status_code=400,
            detail="Characters not yet generated. Call POST /games/{game_id}/characters first.",
        )
    if not db_plot:
        raise HTTPException(
            status_code=400,
            detail="Plot not yet generated. Call POST /games/{game_id}/plot first.",
        )
    if not db_clues:
        raise HTTPException(
            status_code=400,
            detail="Clues not yet generated. Call POST /games/{game_id}/clues first.",
        )
    if not db_metadata:
        raise HTTPException(
            status_code=400,
            detail="Metadata not yet generated. Call POST /games/{game_id}/metadata first.",
        )

    # Convert to Pydantic models
    characters = [
        Character(
            id=char.id,
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
            character_image_path=char.character_image_path,
        )
        for char in db_characters
    ]

    plot = Plot(
        setting=db_plot.setting,
        victim=db_plot.victim,
        crime=db_plot.crime,
        culprit=db_plot.culprit,
        murder_method=db_plot.murder_method,
        timeline=db_plot.timeline,
        resolution=db_plot.resolution,
    )

    clues = [
        Clue(
            clue_id=clue.clue_id,
            description=clue.description,
            location=clue.location,
            revealed_by=clue.revealed_by,
            significance=clue.significance,
            misleading=clue.misleading,
        )
        for clue in db_clues
    ]

    return MysteryScenario(
        title=db_metadata.title,
        theme=game.theme,
        difficulty=game.difficulty,
        num_players=game.num_players,
        estimated_duration=db_metadata.estimated_duration,
        plot=plot,
        characters=characters,
        clues=clues,
        game_instructions=db_metadata.game_instructions,
        introduction=db_metadata.introduction,
    )


@router.delete("/{game_id}", status_code=204)
async def delete_game(game_id: str, db: Session = Depends(get_db)):
    """
    Delete a game and all associated data.

    This will cascade delete all characters, plot, clues, metadata, and validation results.
    """
    success = game_service.delete_game(db, game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")

    return None
