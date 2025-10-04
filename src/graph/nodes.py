"""LangGraph nodes for mystery generation workflow."""

from typing import Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Character, Plot, Clue
from src.config.settings import get_settings
import json


def get_llm() -> ChatAnthropic:
    """Get configured LLM instance."""
    settings = get_settings()
    return ChatAnthropic(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.anthropic_api_key,
    )


def generate_characters_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate characters for the mystery game."""
    llm = get_llm()

    system_prompt = """You are an expert mystery writer creating characters for a murder mystery party game.
Generate diverse, interesting characters with distinct personalities, backgrounds, and secrets.
Each character should have a plausible connection to the mystery."""

    user_prompt = f"""Create {state['num_players']} characters for a mystery party game with the following parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
{f"- Special requests: {state['special_requests']}" if state.get('special_requests') else ""}

For each character, provide:
- name: Full name
- role: Their occupation or role
- background: Brief background story (2-3 sentences)
- personality: Key personality traits
- secret: A hidden secret they're keeping
- motive: A potential motive (for some characters)
- relationship_to_victim: How they know the victim (if applicable)

Return the response as a JSON array of character objects."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Character objects
    try:
        characters_data = json.loads(response.content)
        characters = [Character(**char) for char in characters_data]
        state["characters"] = characters
    except Exception as e:
        print(f"Error parsing characters: {e}")
        state["characters"] = []

    return state


def generate_plot_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate the main plot and storyline."""
    llm = get_llm()

    characters_summary = "\n".join([
        f"- {char.name} ({char.role}): {char.background}"
        for char in state.get("characters", [])
    ])

    system_prompt = """You are an expert mystery writer creating compelling murder mystery plots.
Create a coherent, engaging plot that ties all characters together with a satisfying resolution."""

    user_prompt = f"""Create a murder mystery plot for a party game with these parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}

Characters involved:
{characters_summary}

Provide:
- setting: Detailed setting (time and place)
- victim: Name of the victim (should be one of the characters)
- crime: Description of the crime
- culprit: Who committed the crime (should be one of the characters)
- murder_method: How the crime was committed
- timeline: Array of key events (5-8 events)
- resolution: How the mystery can be solved

Return the response as a JSON object."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    try:
        plot_data = json.loads(response.content)
        plot = Plot(**plot_data)
        state["plot"] = plot
    except Exception as e:
        print(f"Error parsing plot: {e}")
        state["plot"] = None

    return state


def generate_clues_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate clues for the mystery."""
    llm = get_llm()

    plot_summary = ""
    if state.get("plot"):
        plot = state["plot"]
        plot_summary = f"""
Victim: {plot.victim}
Culprit: {plot.culprit}
Method: {plot.murder_method}
Setting: {plot.setting}
"""

    characters_list = ", ".join([char.name for char in state.get("characters", [])])

    system_prompt = """You are an expert mystery writer creating clues for a murder mystery game.
Create a mix of helpful clues and red herrings that make the mystery challenging but solvable."""

    user_prompt = f"""Create clues for a murder mystery game with these parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
- Number of clues: {state['num_players'] + 3}

Plot details:
{plot_summary}

Characters: {characters_list}

For each clue provide:
- clue_id: Unique identifier (e.g., "clue_001")
- description: What the clue is
- location: Where it's found
- revealed_by: Which character has or reveals this clue
- significance: Why it's important
- misleading: Boolean - is this a red herring?

Return the response as a JSON array of clue objects."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    try:
        clues_data = json.loads(response.content)
        clues = [Clue(**clue) for clue in clues_data]
        state["clues"] = clues
    except Exception as e:
        print(f"Error parsing clues: {e}")
        state["clues"] = []

    return state


def generate_metadata_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate title, instructions, and introduction."""
    llm = get_llm()

    system_prompt = """You are an expert game designer creating engaging mystery party games.
Create compelling titles, clear instructions, and atmospheric introductions."""

    user_prompt = f"""Create metadata for a mystery party game:
- Theme: {state['theme']}
- Number of players: {state['num_players']}

Provide:
- title: Catchy title for the game
- estimated_duration: Estimated play time in minutes
- game_instructions: Clear instructions for the game host (2-3 paragraphs)
- introduction: Atmospheric opening scene to set the stage (2-3 paragraphs)

Return as JSON object."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    try:
        metadata = json.loads(response.content)
        state["title"] = metadata.get("title")
        state["estimated_duration"] = metadata.get("estimated_duration")
        state["game_instructions"] = metadata.get("game_instructions")
        state["introduction"] = metadata.get("introduction")
    except Exception as e:
        print(f"Error parsing metadata: {e}")

    return state


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
