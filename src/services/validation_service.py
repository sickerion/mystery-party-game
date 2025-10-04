"""Validation service for CRUD operations on ValidationResult model."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import ValidationResult


def save_validation(
    db: Session,
    game_id: str,
    iteration: int,
    validation_passed: bool,
    validation_errors: Optional[List[str]] = None,
) -> ValidationResult:
    """
    Save a validation result for a game.

    Args:
        db: Database session
        game_id: Game UUID
        iteration: Iteration number
        validation_passed: Whether validation passed
        validation_errors: List of validation error messages

    Returns:
        Created ValidationResult object
    """
    db_validation = ValidationResult(
        game_id=game_id,
        iteration=iteration,
        validation_passed=validation_passed,
        validation_errors=validation_errors,
    )
    db.add(db_validation)
    db.commit()
    db.refresh(db_validation)
    return db_validation


def get_validations_by_game(db: Session, game_id: str) -> List[ValidationResult]:
    """
    Get all validation results for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        List of ValidationResult objects ordered by iteration
    """
    return (
        db.query(ValidationResult)
        .filter(ValidationResult.game_id == game_id)
        .order_by(ValidationResult.iteration)
        .all()
    )


def get_latest_validation(db: Session, game_id: str) -> Optional[ValidationResult]:
    """
    Get the latest validation result for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        Latest ValidationResult object or None if not found
    """
    return (
        db.query(ValidationResult)
        .filter(ValidationResult.game_id == game_id)
        .order_by(ValidationResult.iteration.desc())
        .first()
    )


def delete_validations_by_game(db: Session, game_id: str) -> int:
    """
    Delete all validation results for a game.

    Args:
        db: Database session
        game_id: Game UUID

    Returns:
        Number of validation results deleted
    """
    count = db.query(ValidationResult).filter(ValidationResult.game_id == game_id).delete()
    db.commit()
    return count
