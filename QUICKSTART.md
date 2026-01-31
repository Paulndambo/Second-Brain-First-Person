# Quick Start Guide

## 1. Get Your API Key (30 seconds)

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## 2. Set Up Backend (1 minute)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Set API key (Windows PowerShell)
$env:GEMINI_API_KEY="paste_your_key_here"

# Or Windows CMD
set GEMINI_API_KEY=paste_your_key_here

# Verify setup (optional)
python test_setup.py

# Start server
python main.py
```

Backend will run at: http://localhost:8000

## 3. Set Up Frontend (1 minute)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will run at: http://localhost:5173

## 4. Use the App (30 seconds)

1. Open http://localhost:5173
2. Click "Enable Camera & Microphone"
3. Allow permissions
4. Type your intent (e.g., "I'm preparing for a presentation")
5. Click "Analyze"
6. Wait 3 seconds for recording
7. Get your insight!

## Example Intents to Try

- "I'm trying to focus on work"
- "I'm preparing for a presentation"
- "I'm learning a new concept"
- "I'm about to have a difficult conversation"
- "I'm feeling overwhelmed"

## Troubleshooting

**Backend won't start?**
- Check if API key is set: `echo %GEMINI_API_KEY%`
- Run `python test_setup.py` to verify setup

**Camera not working?**
- Use Chrome or Edge browser
- Check browser permissions
- Make sure you're on localhost (not file://)

**"System uncertain" message?**
- This is normal! The AI only speaks when it has something useful to say
- Try with different lighting or clearer audio
- Make your intent more specific

## Architecture

```
User Intent + Camera + Audio
         ↓
    React Frontend
         ↓
    FastAPI Backend
         ↓
    Gemini 3 API
         ↓
    Single Insight (or silence)
```

## What Makes This Different

- **Not a chatbot** - One question, one insight
- **Multimodal** - Sees and hears your context
- **Smart silence** - Only speaks when helpful
- **Fast** - < 1 second typical response
- **Simple** - No database, no auth, no complexity

---

**Need help?** Check the main README.md for detailed documentation.
