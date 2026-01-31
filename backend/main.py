import os
import base64
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from PIL import Image
import io
import config

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Second Brain, First Person")

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)

# System prompt (hardcoded as specified)
SYSTEM_PROMPT = """You are a real-time cognitive assistant.

You observe situations through images and audio.
Your task is to infer the user's goal and determine whether
a concise intervention would materially improve the outcome.

If no meaningful insight exists, set intervention_needed to false.

Be precise. One insight only."""


class AnalyzeRequest(BaseModel):
    intent: str
    image: Optional[str] = None
    audio: Optional[str] = None


class AnalyzeResponse(BaseModel):
    inferred_goal: str
    confidence: float
    intervention_needed: bool
    insight: str
    suggested_action: str
    why_it_matters: str


def compress_image(base64_image: str, max_size_kb: int = config.MAX_IMAGE_SIZE_KB) -> bytes:
    """Compress image to reduce size while maintaining quality."""
    try:
        # Remove data URL prefix if present
        if "," in base64_image:
            base64_image = base64_image.split(",", 1)[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        # Compress iteratively
        quality = config.IMAGE_QUALITY_START
        output = io.BytesIO()
        
        while quality > config.IMAGE_QUALITY_MIN:
            output.seek(0)
            output.truncate()
            image.save(output, format=config.IMAGE_FORMAT, quality=quality, optimize=True)
            
            if output.tell() <= max_size_kb * 1024:
                break
            
            quality -= 10
        
        return output.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")


def process_audio(base64_audio: str) -> tuple[bytes, str]:
    """Process audio data and detect MIME type."""
    try:
        mime_type = "audio/webm"  # Default
        
        # Remove data URL prefix if present and extract MIME type
        if "," in base64_audio:
            prefix, base64_audio = base64_audio.split(",", 1)
            # Extract MIME type from data URL (e.g., "data:audio/webm;base64")
            if ":" in prefix and ";" in prefix:
                mime_type = prefix.split(":")[1].split(";")[0]
        
        audio_bytes = base64.b64decode(base64_audio)
        return audio_bytes, mime_type
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Audio processing failed: {str(e)}")


@app.get("/")
async def root():
    return { "message": "Server is running and you just found yourself at Second Brain, First Person" }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze user intent with multimodal input (image + audio).
    Returns a single insight if intervention is needed.
    """
    
    # Validate input
    if not request.intent or not request.intent.strip():
        raise HTTPException(status_code=400, detail="Intent is required")
    
    if not request.image:
        raise HTTPException(status_code=400, detail="Image is required")
    
    try:
        # Process multimodal inputs
        image_bytes = compress_image(request.image)
        
        # Prepare content for Gemini
        contents = []
        
        # Add image
        contents.append({
            "mime_type": "image/jpeg",
            "data": image_bytes
        })
        
        # Add audio if provided
        if request.audio:
            audio_bytes, audio_mime_type = process_audio(request.audio)
            contents.append({
                "mime_type": audio_mime_type,
                "data": audio_bytes
            })
        
        # User prompt template
        user_prompt = f"""User intent:
"{request.intent}"

Analyze the current scene and audio.

Respond ONLY in valid JSON using this exact schema:
{{
  "inferred_goal": "string - what the user is trying to accomplish",
  "confidence": 0.0-1.0,
  "intervention_needed": true or false,
  "insight": "string - one concise observation",
  "suggested_action": "string - specific next step",
  "why_it_matters": "string - brief impact explanation"
}}"""
        
        # Call Gemini API
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": config.GEMINI_TEMPERATURE,
                "response_mime_type": "application/json"
            }
        )
        
        response = model.generate_content([
            *contents,
            user_prompt
        ])
        
        # Parse response
        result = json.loads(response.text)
        
        # Apply decision logic
        confidence = float(result.get("confidence", 0.0))
        intervention_needed = result.get("intervention_needed", False)
        
        if not intervention_needed or confidence < config.CONFIDENCE_THRESHOLD:
            # No meaningful insight
            return AnalyzeResponse(
                inferred_goal=result.get("inferred_goal", ""),
                confidence=confidence,
                intervention_needed=False,
                insight="",
                suggested_action="",
                why_it_matters=""
            )
        
        # Return full response
        return AnalyzeResponse(
            inferred_goal=result.get("inferred_goal", ""),
            confidence=confidence,
            intervention_needed=True,
            insight=result.get("insight", ""),
            suggested_action=result.get("suggested_action", ""),
            why_it_matters=result.get("why_it_matters", "")
        )
        
    except json.JSONDecodeError:
        # Gemini response parsing failed
        return AnalyzeResponse(
            inferred_goal="",
            confidence=0.0,
            intervention_needed=False,
            insight="",
            suggested_action="",
            why_it_matters="System uncertain, try again."
        )
    except Exception as e:
        # Any other error
        print(f"Error: {str(e)}")
        return AnalyzeResponse(
            inferred_goal="",
            confidence=0.0,
            intervention_needed=False,
            insight="",
            suggested_action="",
            why_it_matters="System uncertain, try again."
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
