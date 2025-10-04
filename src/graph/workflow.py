"""LangGraph workflow definition for mystery generation."""

from langgraph.graph import StateGraph, END
from src.models.state import MysteryGenerationState
from src.graph.nodes import (
    generate_characters_node,
    generate_plot_node,
    generate_clues_node,
    generate_metadata_node,
    validate_scenario_node,
)


def should_retry(state: MysteryGenerationState) -> str:
    """Determine if we should retry generation or finish."""
    if state.get("validation_passed"):
        return "end"

    # Limit retries
    if state.get("iteration_count", 0) >= 2:
        return "end"

    return "retry"


def create_mystery_graph() -> StateGraph:
    """Create the LangGraph workflow for mystery generation."""

    # Create the graph
    workflow = StateGraph(MysteryGenerationState)

    # Add nodes
    workflow.add_node("generate_characters", generate_characters_node)
    workflow.add_node("generate_plot", generate_plot_node)
    workflow.add_node("generate_clues", generate_clues_node)
    workflow.add_node("generate_metadata", generate_metadata_node)
    workflow.add_node("validate", validate_scenario_node)

    # Define the flow
    workflow.set_entry_point("generate_characters")

    workflow.add_edge("generate_characters", "generate_plot")
    workflow.add_edge("generate_plot", "generate_clues")
    workflow.add_edge("generate_clues", "generate_metadata")
    workflow.add_edge("generate_metadata", "validate")

    # Add conditional edge from validate
    workflow.add_conditional_edges(
        "validate",
        should_retry,
        {
            "retry": "generate_characters",
            "end": END,
        }
    )

    return workflow.compile()


def generate_mystery_scenario(
    theme: str,
    num_players: int,
    difficulty: str,
    special_requests: str = None
) -> MysteryGenerationState:
    """
    Generate a complete mystery party game scenario.

    Args:
        theme: Theme for the mystery
        num_players: Number of players (3-12)
        difficulty: Difficulty level (easy, medium, hard)
        special_requests: Optional special requests

    Returns:
        MysteryGenerationState with complete scenario
    """
    # Initialize state
    initial_state: MysteryGenerationState = {
        "theme": theme,
        "num_players": num_players,
        "difficulty": difficulty,
        "special_requests": special_requests,
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

    # Create and run the graph
    graph = create_mystery_graph()
    result = graph.invoke(initial_state)

    return result
