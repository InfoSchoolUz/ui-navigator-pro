import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PlanRequest, PlanResponse
from .gemini_client import GeminiPlanner

app = FastAPI(title="UI Navigator Agent", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = None

@app.on_event("startup")
def _startup():
    global planner
    try:
        planner = GeminiPlanner()
    except Exception as e:
        # still allow /health
        print("Startup error:", e)

@app.get("/health")
def health():
    return {"ok": True, "planner_ready": planner is not None}

@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest):
    if planner is None:
        raise HTTPException(status_code=500, detail="Planner not initialized (missing GEMINI_API_KEY?)")
    try:
        return planner.plan(
            intent=req.intent,
            screenshot_b64=req.screenshot_b64,
            w=req.screenshot_width,
            h=req.screenshot_height,
            audio_wav_b64=req.audio_wav_b64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))