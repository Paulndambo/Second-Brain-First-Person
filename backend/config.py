"""
Configuration settings for Second Brain, First Person
"""

# API Configuration
GEMINI_MODEL = "gemini-2.5-flash-lite"
GEMINI_TEMPERATURE = 0.4

# Image Processing
MAX_IMAGE_SIZE_KB = 500
IMAGE_FORMAT = "JPEG"
IMAGE_QUALITY_START = 85
IMAGE_QUALITY_MIN = 20

# Audio Recording
AUDIO_DURATION_SECONDS = 3
AUDIO_MIME_TYPE = "audio/webm"

# Decision Thresholds
CONFIDENCE_THRESHOLD = 0.7

# CORS Settings
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Server Settings
HOST = "0.0.0.0"
PORT = 8000
