"""Generation API router - incremental mystery generation endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models import GameStatus
from src.models.schema import Character, Plot, Clue
from src.services import (
    game_service,
    character_service,
    plot_service,
    clue_service,
    metadata_service,
    validation_service,
)
from src.graph.nodes.characters import generate_characters_node
from src.graph.nodes.plot import generate_plot_node
from src.graph.nodes.clues import generate_clues_node
from src.graph.nodes.metadata import generate_metadata_node
from src.graph.nodes.validation import validate_scenario_node
from src.models.state import MysteryGenerationState

router = APIRouter(prefix="/games", tags=["generation"])


# Response models
from pydantic import BaseModel


class MetadataResponse(BaseModel):
    """Response for metadata generation."""
    title: str
    estimated_duration: int
    game_instructions: str
    introduction: str


class ValidationResponse(BaseModel):
    """Response for validation."""
    validation_passed: bool
    validation_errors: List[str] = []
    iteration: int


@router.post("/{game_id}/characters", response_model=List[Character])
async def generate_characters(game_id: str, db: Session = Depends(get_db)):
    """
    Generate characters for a game.

    Calls the character generation node and saves results to database.
    Updates game status to CHARACTERS_GENERATED.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Prepare state for character generation
    state: MysteryGenerationState = {
        "theme": game.theme,
        "num_players": game.num_players,
        "difficulty": game.difficulty,
        "special_requests": game.special_requests,
        "language": game.language,
        "characters": None,
        "plot": None,
        "clues": None,
        "title": None,
        "estimated_duration": None,
        "game_instructions": None,
        "introduction": None,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    # Generate characters
    result_state = generate_characters_node(state)

    if not result_state.get("characters"):
        raise HTTPException(
            status_code=500,
            detail="Failed to generate characters",
        )

    # Save to database
    characters = result_state["characters"]
    db_characters = character_service.save_characters(db, game_id, characters)

    # Update game status
    game_service.update_game_status(db, game_id, GameStatus.CHARACTERS_GENERATED)

    # Convert DB characters back to Pydantic models with IDs
    characters_with_ids = []
    for db_char in db_characters:
        char_dict = {
            "id": db_char.id,
            "name": db_char.name,
            "role": db_char.role,
            "background": db_char.background,
            "personality": db_char.personality,
            "secret": db_char.secret,
            "motive": db_char.motive,
            "relationship_to_victim": db_char.relationship_to_victim,
        }
        characters_with_ids.append(Character(**char_dict))

    return characters_with_ids


@router.post("/{game_id}/plot", response_model=Plot)
async def generate_plot(game_id: str, db: Session = Depends(get_db)):
    """
    Generate plot for a game.

    Requires characters to be generated first.
    Calls the plot generation node and saves results to database.
    Updates game status to PLOT_GENERATED.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check that characters exist
    db_characters = character_service.get_characters_by_game(db, game_id)
    if not db_characters:
        raise HTTPException(
            status_code=400,
            detail="Characters must be generated first. Call POST /games/{game_id}/characters",
        )

    # Convert DB characters to Pydantic models
    characters = [
        Character(
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
        )
        for char in db_characters
    ]

    # Prepare state for plot generation
    state: MysteryGenerationState = {
        "theme": game.theme,
        "num_players": game.num_players,
        "difficulty": game.difficulty,
        "special_requests": game.special_requests,
        "language": game.language,
        "characters": characters,
        "plot": None,
        "clues": None,
        "title": None,
        "estimated_duration": None,
        "game_instructions": None,
        "introduction": None,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    # Generate plot
    result_state = generate_plot_node(state)

    if not result_state.get("plot"):
        raise HTTPException(
            status_code=500,
            detail="Failed to generate plot",
        )

    # Save to database
    plot = result_state["plot"]
    plot_service.save_plot(db, game_id, plot)

    # Update game status
    game_service.update_game_status(db, game_id, GameStatus.PLOT_GENERATED)

    return plot


@router.post("/{game_id}/clues", response_model=List[Clue])
async def generate_clues(game_id: str, db: Session = Depends(get_db)):
    """
    Generate clues for a game.

    Requires characters and plot to be generated first.
    Calls the clues generation node and saves results to database.
    Updates game status to CLUES_GENERATED.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check that characters and plot exist
    db_characters = character_service.get_characters_by_game(db, game_id)
    db_plot = plot_service.get_plot_by_game(db, game_id)

    if not db_characters:
        raise HTTPException(
            status_code=400,
            detail="Characters must be generated first. Call POST /games/{game_id}/characters",
        )
    if not db_plot:
        raise HTTPException(
            status_code=400,
            detail="Plot must be generated first. Call POST /games/{game_id}/plot",
        )

    # Convert to Pydantic models
    characters = [
        Character(
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
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

    # Prepare state for clues generation
    state: MysteryGenerationState = {
        "theme": game.theme,
        "num_players": game.num_players,
        "difficulty": game.difficulty,
        "special_requests": game.special_requests,
        "language": game.language,
        "characters": characters,
        "plot": plot,
        "clues": None,
        "title": None,
        "estimated_duration": None,
        "game_instructions": None,
        "introduction": None,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    # Generate clues
    result_state = generate_clues_node(state)

    if not result_state.get("clues"):
        raise HTTPException(
            status_code=500,
            detail="Failed to generate clues",
        )

    # Save to database
    clues = result_state["clues"]
    clue_service.save_clues(db, game_id, clues)

    # Update game status
    game_service.update_game_status(db, game_id, GameStatus.CLUES_GENERATED)

    return clues


@router.post("/{game_id}/metadata", response_model=MetadataResponse)
async def generate_metadata(game_id: str, db: Session = Depends(get_db)):
    """
    Generate metadata (title, instructions, introduction) for a game.

    Requires characters, plot, and clues to be generated first.
    Calls the metadata generation node and saves results to database.
    Updates game status to METADATA_GENERATED.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check that all components exist
    db_characters = character_service.get_characters_by_game(db, game_id)
    db_plot = plot_service.get_plot_by_game(db, game_id)
    db_clues = clue_service.get_clues_by_game(db, game_id)

    if not db_characters:
        raise HTTPException(
            status_code=400,
            detail="Characters must be generated first",
        )
    if not db_plot:
        raise HTTPException(
            status_code=400,
            detail="Plot must be generated first",
        )
    if not db_clues:
        raise HTTPException(
            status_code=400,
            detail="Clues must be generated first",
        )

    # Convert to Pydantic models
    characters = [
        Character(
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
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

    # Prepare state for metadata generation
    state: MysteryGenerationState = {
        "theme": game.theme,
        "num_players": game.num_players,
        "difficulty": game.difficulty,
        "special_requests": game.special_requests,
        "language": game.language,
        "characters": characters,
        "plot": plot,
        "clues": clues,
        "title": None,
        "estimated_duration": None,
        "game_instructions": None,
        "introduction": None,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    # Generate metadata
    result_state = generate_metadata_node(state)

    if not result_state.get("title"):
        raise HTTPException(
            status_code=500,
            detail="Failed to generate metadata",
        )

    # Save to database
    metadata_service.save_metadata(
        db,
        game_id,
        title=result_state["title"],
        estimated_duration=result_state["estimated_duration"],
        game_instructions=result_state["game_instructions"],
        introduction=result_state["introduction"],
    )

    # Update game status
    game_service.update_game_status(db, game_id, GameStatus.METADATA_GENERATED)

    return MetadataResponse(
        title=result_state["title"],
        estimated_duration=result_state["estimated_duration"],
        game_instructions=result_state["game_instructions"],
        introduction=result_state["introduction"],
    )


@router.post("/{game_id}/validate", response_model=ValidationResponse)
async def validate_scenario(game_id: str, db: Session = Depends(get_db)):
    """
    Validate the complete game scenario.

    Requires all components (characters, plot, clues, metadata) to be generated first.
    Calls the validation node and saves results to database.
    Updates game status to VALIDATED or FAILED based on validation result.
    """
    game = game_service.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check that all components exist
    db_characters = character_service.get_characters_by_game(db, game_id)
    db_plot = plot_service.get_plot_by_game(db, game_id)
    db_clues = clue_service.get_clues_by_game(db, game_id)
    db_metadata = metadata_service.get_metadata_by_game(db, game_id)

    if not db_characters:
        raise HTTPException(status_code=400, detail="Characters must be generated first")
    if not db_plot:
        raise HTTPException(status_code=400, detail="Plot must be generated first")
    if not db_clues:
        raise HTTPException(status_code=400, detail="Clues must be generated first")
    if not db_metadata:
        raise HTTPException(status_code=400, detail="Metadata must be generated first")

    # Convert to Pydantic models
    characters = [
        Character(
            name=char.name,
            role=char.role,
            background=char.background,
            personality=char.personality,
            secret=char.secret,
            motive=char.motive,
            relationship_to_victim=char.relationship_to_victim,
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

    # Get current iteration count
    existing_validations = validation_service.get_validations_by_game(db, game_id)
    iteration = len(existing_validations) + 1

    # Prepare state for validation
    state: MysteryGenerationState = {
        "theme": game.theme,
        "num_players": game.num_players,
        "difficulty": game.difficulty,
        "special_requests": game.special_requests,
        "language": game.language,
        "characters": characters,
        "plot": plot,
        "clues": clues,
        "title": db_metadata.title,
        "estimated_duration": db_metadata.estimated_duration,
        "game_instructions": db_metadata.game_instructions,
        "introduction": db_metadata.introduction,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": iteration - 1,
    }

    # Validate
    result_state = validate_scenario_node(state)

    # Save validation result
    validation_service.save_validation(
        db,
        game_id,
        iteration=iteration,
        validation_passed=result_state["validation_passed"],
        validation_errors=result_state.get("validation_errors"),
    )

    # Update game status
    if result_state["validation_passed"]:
        game_service.update_game_status(db, game_id, GameStatus.VALIDATED)
    else:
        game_service.update_game_status(db, game_id, GameStatus.FAILED)

    return ValidationResponse(
        validation_passed=result_state["validation_passed"],
        validation_errors=result_state.get("validation_errors") or [],
        iteration=iteration,
    )
