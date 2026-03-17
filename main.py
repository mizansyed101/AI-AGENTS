import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from finance_agent import generate_financial_plan
import uvicorn

app = FastAPI(title="AI Personal Finance Planner")

# NOTE: Ensure 'GEMINI_API_KEY' is set in your environment variables.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class PlanRequest(BaseModel):
    financial_goals: str
    current_situation: str

@app.post("/api/plan")
async def create_plan(request: PlanRequest):
    if not request.financial_goals or not request.current_situation:
        raise HTTPException(status_code=400, detail="Financial goals and situation are required.")
        
    try:
        plan = generate_financial_plan(
            gemini_api_key=GEMINI_API_KEY,
            financial_goals=request.financial_goals,
            current_situation=request.current_situation
        )
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
