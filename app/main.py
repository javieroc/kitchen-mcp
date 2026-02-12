"""FastAPI routes for Kitchen Orchestration."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .agent import get_recipe_recommendation

app = FastAPI(title="Kitchen Orchestrator API", version="0.1.0")


@app.get("/")
async def root():
    """Welcome endpoint."""
    return JSONResponse({
        "message": "Kitchen Orchestrator API",
        "version": "0.1.0",
        "status": "running"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "kitchen-orchestrator"
    })


@app.get("/recipe/recommend")
async def recommend_recipe(ingredients: str = None):
    """
    Get recipe recommendations based on available ingredients.

    Args:
        ingredients: Comma-separated list of available ingredients
    """
    recommendation = get_recipe_recommendation(ingredients)
    return JSONResponse(recommendation)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
