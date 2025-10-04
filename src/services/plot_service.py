"""Plot service for CRUD operations on GeneratedPlot model."""

from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import GeneratedPlot
from src.models.schema import Plot


def save_plot(db: Session, game_id: str, plot: Plot) -> GeneratedPlot:
    """
    Save or update plot for a game.

    Args:
        db: Database session
        game_id: Game UUID
        plot: Plot object from Pydantic

    Returns:
        Created or updated GeneratedPlot object
    """
    # Check if plot already exists
    existing_plot = get_plot_by_game(db, game_id)

    if existing_plot:
        # Update existing plot
        existing_plot.setting = plot.setting
        existing_plot.victim = plot.victim
        existing_plot.crime = plot.crime
        existing_plot.culprit = plot.culprit
        existing_plot.murder_method = plot.murder_method
        existing_plot.timeline = plot.timeline
        existing_plot.resolution = plot.resolution
        db.commit()
        db.refresh(existing_plot)
        return existing_plot
    else:
        # Create new plot
        db_plot = GeneratedPlot(
            game_id=game_id,
            setting=plot.setting,
            victim=plot.victim,
            crime=plot.crime,
            culprit=plot.culprit,
            murder_method=plot.murder_method,
            timeline=plot.timeline,
            resolution=plot.resolution,
        )
        db.add(db_plot)
        db.commit()
        db.refresh(db_plot)
        return db_plot


def get_plot_by_game(db: Session, game_id: str) -> Optional[GeneratedPlot]:
    """
    Get plot for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        GeneratedPlot object or None if not found
    """
    return db.query(GeneratedPlot).filter(GeneratedPlot.game_id == game_id).first()


def delete_plot_by_game(db: Session, game_id: str) -> bool:
    """
    Delete plot for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        True if deleted, False if not found
    """
    plot = get_plot_by_game(db, game_id)
    if plot:
        db.delete(plot)
        db.commit()
        return True
    return False
