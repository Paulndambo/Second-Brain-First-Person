# Second Brain, First Person

A real-time multimodal cognitive assistant powered by the Gemini 3 API. This is a hackathon MVP that analyzes your environment through camera and audio to provide contextual insights when you need them.

## What It Does

This is **NOT** a chat application. It's a **single-insight, real-time assistant** that:

1. Captures one frame from your camera
2. Records 3 seconds of audio
3. Analyzes your stated intent with multimodal context
4. Provides **one concise insight** if intervention would help
5. Stays silent if everything looks good

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Gemini 3 API** - Multimodal AI (image + audio analysis)
- **Pillow** - Image compression
- **Uvicorn** - ASGI server

### Frontend
- **React** - Single Page Application
- **Vite** - Build tool
- **getUserMedia API** - Camera & microphone access

## Quick Start (< 60 seconds)

### Prerequisites

- Python 3.10+
- Node.js 16+
- Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone and navigate to the project:**
```bash
cd FirstPersonSecondBrain
```

2. **Set up the backend:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure your API key:**
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_actual_api_key_here"

# Windows (CMD)
set GEMINI_API_KEY=your_actual_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_actual_api_key_here
```

4. **Start the backend server:**
```bash
python main.py
```
The API will be available at `http://localhost:8000`

5. **In a new terminal, set up the frontend:**
```bash
cd frontend
npm install
npm run dev
```
The app will open at `http://localhost:5173`

### Demo in 60 Seconds

1. Open `http://localhost:5173` in your browser
2. Click **"Enable Camera & Microphone"** and allow permissions
3. Type your intent (e.g., "I'm trying to focus on work")
4. Click **"Analyze"**
5. Wait 3 seconds while it records audio
6. Get your insight (or silence if no intervention needed)

## How It Works

### Gemini 3 Integration

The system uses Gemini's multimodal capabilities to analyze:
- **Visual context** - One compressed JPEG frame (<500KB)
- **Audio context** - 3 seconds of WebM audio
- **User intent** - Your stated goal

### System Prompt

```
You are a real-time cognitive assistant.

You observe situations through images and audio.
Your task is to infer the user's goal and determine whether
a concise intervention would materially improve the outcome.

If no meaningful insight exists, set intervention_needed to false.

Be precise. One insight only.
```

### Decision Logic

The assistant only responds when:
- `intervention_needed == true` **AND**
- `confidence >= 0.7`

Otherwise, it stays silent.

## API Reference

### POST /analyze

**Request:**
```json
{
  "intent": "What you're trying to accomplish",
  "image": "base64-encoded JPEG",
  "audio": "base64-encoded WebM audio"
}
```

**Response:**
```json
{
  "inferred_goal": "What the system thinks you're doing",
  "confidence": 0.85,
  "intervention_needed": true,
  "insight": "One concise observation",
  "suggested_action": "Specific next step",
  "why_it_matters": "Brief impact explanation"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Project Structure

```
FirstPersonSecondBrain/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── env.example             # Environment variables template
└── README.md              # This file
```

## Features

✅ Real-time camera capture
✅ 3-second audio recording
✅ Multimodal analysis (image + audio + text)
✅ Single concise insight
✅ Confidence scoring
✅ Smart silence (no unnecessary responses)
✅ Modern, responsive UI
✅ < 1 second response time (typically)

## Non-Features (By Design)

❌ No chat history
❌ No user authentication
❌ No database
❌ No streaming responses
❌ No long-term memory
❌ No background processing
❌ No multiple suggestions

## Latency & Cost Optimization

- **Single image per request** - One frame, not video stream
- **Image compression** - Automatically compressed to <500KB
- **No retries** - One API call per interaction
- **Smart thresholding** - Only responds when confident (≥70%)

## Troubleshooting

### Camera/Microphone Not Working
- Ensure you're using HTTPS or localhost
- Check browser permissions
- Try a different browser (Chrome/Edge recommended)

### Backend Errors
- Verify `GEMINI_API_KEY` is set correctly
- Check API quota at [Google AI Studio](https://aistudio.google.com/)
- Ensure Python 3.10+ is installed

### CORS Issues
- Backend must be running on port 8000
- Frontend must be on port 5173 or 3000
- Check CORS middleware in `main.py`

## Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

## License

MIT License - This is a hackathon MVP, use freely!

## Credits

Built with:
- [Gemini API](https://ai.google.dev/) - Multimodal AI
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [React](https://react.dev/) - UI library
- [Vite](https://vitejs.dev/) - Build tool

---

**Note:** This is a hackathon MVP focused on speed and simplicity. It demonstrates multimodal AI capabilities without over-engineering.
