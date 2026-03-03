from pydantic import BaseModel, Field, conlist
from typing import Literal, Optional, List, Dict, Any


class PlanRequest(BaseModel):
    intent: str = Field(..., description="User goal in natural language")
    screenshot_b64: str = Field(..., description="PNG/JPG base64 (no data: prefix)")
    screenshot_width: int = Field(..., ge=1)
    screenshot_height: int = Field(..., ge=1)

    # optional audio (wav pcm16 16k mono) base64
    audio_wav_b64: Optional[str] = None


ActionType = Literal["click", "double_click", "right_click", "type", "press", "scroll", "wait"]


class Action(BaseModel):
    type: ActionType
    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    key: Optional[str] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    ms: Optional[int] = None
    reason: str = ""


class PlanResponse(BaseModel):
    goal: str
    actions: List[Action]
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    notes: str = ""
    meta: Dict[str, Any] = Field(default_factory=dict)