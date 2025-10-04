"""Validation node."""

from src.models.state import MysteryGenerationState


def validate_scenario_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Validate the generated scenario for coherence and completeness."""
    errors = []

    # Check if all required components exist
    if not state.get("characters"):
        errors.append("No characters generated")
    elif len(state["characters"]) != state["num_players"]:
        errors.append(f"Expected {state['num_players']} characters, got {len(state['characters'])}")

    if not state.get("plot"):
        errors.append("No plot generated")
    else:
        plot = state["plot"]
        # Verify victim and culprit are among characters
        character_names = [c.name for c in state.get("characters", [])]
        if plot.victim not in character_names:
            errors.append(f"Victim '{plot.victim}' is not in character list")
        if plot.culprit not in character_names:
            errors.append(f"Culprit '{plot.culprit}' is not in character list")

    if not state.get("clues"):
        errors.append("No clues generated")
    elif len(state["clues"]) < 3:
        errors.append("Too few clues generated")

    if not state.get("title"):
        errors.append("No title generated")

    # Set validation status
    state["validation_passed"] = len(errors) == 0
    state["validation_errors"] = errors if errors else None

    return state
