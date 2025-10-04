"""Plot generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Plot
from src.graph.nodes.utils import get_llm


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

Living player characters (all playable suspects/investigators):
{characters_summary}

Provide a JSON object with these exact fields:
- setting: STRING - Setting description (2 sentences max)
- victim: STRING - Name of the victim (must be an NPC, NOT one of the player characters above)
- crime: STRING - Description of the crime (1 sentence)
- culprit: STRING - Name of the culprit (MUST be one of the player characters above)
- murder_method: STRING - How the crime was committed (1 sentence)
- timeline: ARRAY of STRINGS - 5-7 key events (brief, 1 sentence each)
- resolution: STRING - How the mystery can be solved (2-3 sentences max)

CRITICAL: Keep ALL descriptions CONCISE (1-3 sentences) to ensure complete JSON response.
Return ONLY valid JSON, nothing else.

Example format:
{{
  "setting": "A Victorian mansion during a thunderstorm. Guests are trapped inside.",
  "victim": "Lord Blackwood",
  "crime": "Poisoned during dinner",
  "culprit": "Lady Smith",
  "murder_method": "Arsenic in the wine",
  "timeline": ["Guest arrive at 6pm", "Dinner served at 7pm", "Victim collapses at 8pm"],
  "resolution": "The poisoned wine glass has fingerprints matching the culprit."
}}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Plot object
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
        plot_data = json.loads(content)
        plot = Plot(**plot_data)
        state["plot"] = plot
    except json.JSONDecodeError as e:
        print(f"Error parsing plot: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")

        # Try to salvage partial JSON by finding the last complete closing brace
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to find the last valid closing brace
            last_brace = content.rfind('}')
            if last_brace > 0:
                # Try parsing up to the last brace
                truncated_content = content[:last_brace + 1]
                plot_data = json.loads(truncated_content)
                plot = Plot(**plot_data)
                state["plot"] = plot
                print(f"Successfully recovered plot from partial JSON")
                return state
        except Exception as recovery_error:
            print(f"Recovery attempt failed: {recovery_error}")

        state["plot"] = None
    except Exception as e:
        print(f"Unexpected error parsing plot: {e}")
        print(f"Response content: {response.content[:1000]}")
        state["plot"] = None

    return state
