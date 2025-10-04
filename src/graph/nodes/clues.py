"""Clues generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Clue
from src.graph.nodes.utils import get_llm


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
- description: What the clue is (1-2 sentences, keep concise)
- location: Where it's found (brief)
- revealed_by: Which character has or reveals this clue
- significance: Why it's important (1 sentence)
- misleading: Boolean - is this a red herring?

IMPORTANT: Keep all descriptions CONCISE (1-2 sentences max) to ensure the complete JSON response.
Return ONLY a valid JSON array, nothing else.

Example format:
[
  {{
    "clue_id": "clue_001",
    "description": "A torn letter fragment found in the fireplace.",
    "location": "Study fireplace",
    "revealed_by": "John Smith",
    "significance": "Shows victim was being blackmailed.",
    "misleading": false
  }}
]"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Clue objects
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
        clues_data = json.loads(content)

        # Handle both array and object with "clues" key
        if isinstance(clues_data, dict) and "clues" in clues_data:
            clues_data = clues_data["clues"]

        clues = [Clue(**clue) for clue in clues_data]
        state["clues"] = clues
    except json.JSONDecodeError as e:
        print(f"Error parsing clues: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")

        # Try to salvage partial JSON by finding the last complete object
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to find the last valid closing bracket
            last_bracket = content.rfind(']')
            if last_bracket > 0:
                # Try parsing up to the last bracket
                truncated_content = content[:last_bracket + 1]
                clues_data = json.loads(truncated_content)

                if isinstance(clues_data, dict) and "clues" in clues_data:
                    clues_data = clues_data["clues"]

                clues = [Clue(**clue) for clue in clues_data]
                state["clues"] = clues
                print(f"Successfully recovered {len(clues)} clues from partial JSON")
                return state
        except Exception as recovery_error:
            print(f"Recovery attempt failed: {recovery_error}")

        state["clues"] = []
    except Exception as e:
        print(f"Unexpected error parsing clues: {e}")
        print(f"Response content: {response.content[:1000]}")
        state["clues"] = []

    return state
