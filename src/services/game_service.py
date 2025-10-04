"""Game service for CRUD operations on Game model."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Game, GameStatus


def create_game(
    db: Session,
    theme: str,
    num_players: int,
    difficulty: str,
    special_requests: Optional[str] = None,
    language: str = "en",
) -> Game:
    """
    Create a new game.

    Args:
        db: Database session
        theme: Theme of the mystery
        num_players: Number of players
        difficulty: Difficulty level (easy, medium, hard)
        special_requests: Optional special requests
        language: Language for generated content (en or fr)

    Returns:
        Created Game object
    """
    game = Game(
        theme=theme,
        num_players=num_players,
        difficulty=difficulty,
        special_requests=special_requests,
        language=language,
        status=GameStatus.INITIALIZED,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def get_game(db: Session, game_id: str) -> Optional[Game]:
    """
    Get a game by ID.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        Game object or None if not found
    """
    return db.query(Game).filter(Game.id == game_id).first()


def update_game_status(db: Session, game_id: str, status: GameStatus) -> Optional[Game]:
    """
    Update game status.

    Args:
        db: Database session
        game_id: Game UUID
        status: New status

    Returns:
        Updated Game object or None if not found
    """
    game = get_game(db, game_id)
    if game:
        game.status = status
        db.commit()
        db.refresh(game)
    return game


def list_games(
    db: Session,
    status: Optional[GameStatus] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Game]:
    """
    List games with optional filtering.

    Args:
        db: Database session
        status: Optional status filter
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        List of Game objects
    """
    query = db.query(Game)

    if status:
        query = query.filter(Game.status == status)

    query = query.order_by(Game.created_at.desc())
    query = query.limit(limit).offset(offset)

    return query.all()


def delete_game(db: Session, game_id: str) -> bool:
    """
    Delete a game and all related data (cascade).

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        True if deleted, False if not found
    """
    game = get_game(db, game_id)
    if game:
        db.delete(game)
        db.commit()
        return True
    return False
