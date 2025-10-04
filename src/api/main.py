"""FastAPI main application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.schema import GameRequest, MysteryScenario
from src.graph.workflow import generate_mystery_scenario
from src.api.routers import games, generation

app = FastAPI(
    title="Mystery Party Game Generator API",
    description="AI-powered mystery party game generator using LangGraph and Anthropic Claude",
    version="0.2.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(games.router)
app.include_router(generation.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Mystery Party Game Generator API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate", response_model=MysteryScenario)
async def generate_mystery(request: GameRequest):
    """
    Generate a complete mystery party game scenario.

    Args:
        request: GameRequest containing theme, num_players, difficulty, and optional special_requests

    Returns:
        MysteryScenario: Complete mystery game scenario

    Raises:
        HTTPException: If generation fails or validation errors occur
    """
    try:
        # Generate the mystery scenario
        result = generate_mystery_scenario(
            theme=request.theme,
            num_players=request.num_players,
            difficulty=request.difficulty,
            special_requests=request.special_requests,
        )

        # Check if validation passed
        if not result.get("validation_passed"):
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Failed to generate valid scenario",
                    "errors": result.get("validation_errors", []),
                },
            )

        # Build the response
        scenario = MysteryScenario(
            title=result["title"],
            theme=result["theme"],
            difficulty=result["difficulty"],
            num_players=result["num_players"],
            estimated_duration=result["estimated_duration"],
            plot=result["plot"],
            characters=result["characters"],
            clues=result["clues"],
            game_instructions=result["game_instructions"],
            introduction=result["introduction"],
        )

        return scenario

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        )
