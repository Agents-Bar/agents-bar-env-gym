from fastapi import FastAPI

from app.env import router as env_router

# Initiate module with setting up a server
app = FastAPI(
    title="Agents Bar - Environment",
    description="Agents Bar compatible Environment entity",
    docs_url="/docs",
)

@app.get("/ping", response_model=str)
def ping():
    """Diagnostic tool. Make sure that http server is running"""
    return "All good"

app.include_router(env_router)
