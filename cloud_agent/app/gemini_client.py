import base64
import json
import os
from typing import Tuple

from google import genai
from google.genai import types

from .schemas import PlanResponse
from .prompts import SYSTEM_INSTRUCTIONS, USER_TEMPLATE


def _b64_to_bytes(b64: str) -> bytes:
    return base64.b64decode(b64.encode("utf-8"))


def _safe_json_extract(text: str) -> str:
    """
    Model sometimes wraps JSON in markdown. Strip safely.
    """
    t = text.strip()
    if t.startswith("```"):
        # remove fences
        t = t.split("```", 2)[1] if "```" in t else t
        t = t.replace("json", "").strip()
    # best effort: find first { and last }
    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start:end+1]
    return t


class GeminiPlanner:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY missing in environment.")
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("PLANNER_MODEL_ID", "gemini-2.5-flash")

    def plan(self, intent: str, screenshot_b64: str, w: int, h: int, audio_wav_b64: str | None = None) -> PlanResponse:
        img_bytes = _b64_to_bytes(screenshot_b64)

        parts = [
            types.Part(text=SYSTEM_INSTRUCTIONS),
            types.Part(text=USER_TEMPLATE.format(intent=intent, w=w, h=h)),
            types.Part(inline_data=types.Blob(mime_type="image/png", data=img_bytes)),
        ]

        # Optional audio: helps "voice intent"
        if audio_wav_b64:
            audio_bytes = _b64_to_bytes(audio_wav_b64)
            parts.append(types.Part(inline_data=types.Blob(mime_type="audio/wav", data=audio_bytes)))

        resp = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=1200,
            ),
        )

        text = (resp.text or "").strip()
        if not text:
            raise RuntimeError("Empty response from model.")

        raw_json = _safe_json_extract(text)

        # Parse with retry if needed
        try:
            data = json.loads(raw_json)
            return PlanResponse(**data)
        except Exception:
            # one retry: ask model to output strict JSON only
            retry_parts = [
                types.Part(text=SYSTEM_INSTRUCTIONS),
                types.Part(text="Your previous output was invalid JSON. Output ONLY valid JSON, no markdown."),
                types.Part(text=USER_TEMPLATE.format(intent=intent, w=w, h=h)),
                types.Part(inline_data=types.Blob(mime_type="image/png", data=img_bytes)),
            ]
            if audio_wav_b64:
                retry_parts.append(types.Part(inline_data=types.Blob(mime_type="audio/wav", data=_b64_to_bytes(audio_wav_b64))))

            resp2 = self.client.models.generate_content(
                model=self.model,
                contents=[types.Content(role="user", parts=retry_parts)],
                config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=1200),
            )
            text2 = (resp2.text or "").strip()
            raw_json2 = _safe_json_extract(text2)
            data2 = json.loads(raw_json2)
            return PlanResponse(**data2)