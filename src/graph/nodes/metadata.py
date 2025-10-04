"""Metadata generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.graph.nodes.utils import get_llm


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

    # Parse the response and extract metadata
    try:
        content = response.content

        # Try to extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Remove any leading/trailing whitespace
        content = content.strip()

        # Parse JSON
        metadata = json.loads(content)
        state["title"] = metadata.get("title")
        state["estimated_duration"] = metadata.get("estimated_duration")
        state["game_instructions"] = metadata.get("game_instructions")
        state["introduction"] = metadata.get("introduction")
    except json.JSONDecodeError as e:
        print(f"Error parsing metadata: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")
    except Exception as e:
        print(f"Unexpected error parsing metadata: {e}")
        print(f"Response content: {response.content[:1000]}")

    return state
