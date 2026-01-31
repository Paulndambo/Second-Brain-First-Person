# Troubleshooting Guide

## Common Issues and Solutions

---

### 🔴 Backend Won't Start

#### Error: "GEMINI_API_KEY environment variable not set"

**Solution:**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_actual_key_here"

# Windows CMD
set GEMINI_API_KEY=your_actual_key_here

# Verify it's set
echo %GEMINI_API_KEY%
```

**Get API Key:** https://aistudio.google.com/app/apikey

---

#### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

**Verify installation:**
```bash
python test_setup.py
```

---

#### Error: Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in backend/config.py
PORT = 8001
```

---

### 🔴 Frontend Issues

#### Error: "npm: command not found"

**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart terminal
3. Verify: `node --version`

---

#### Error: Cannot connect to backend

**Symptoms:**
- "Failed to fetch"
- "Network error"
- CORS errors in console

**Solution:**
1. Ensure backend is running on port 8000
2. Check backend logs for errors
3. Verify CORS settings in `backend/main.py`
4. Try accessing http://localhost:8000/health directly

---

#### Error: npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

### 🔴 Camera/Microphone Issues

#### Camera permission denied

**Solution:**
1. Use Chrome or Edge (best compatibility)
2. Ensure you're on `localhost` (not `file://`)
3. Check browser permissions:
   - Chrome: Settings → Privacy → Site Settings → Camera
   - Edge: Settings → Cookies and site permissions → Camera
4. Try different browser
5. Restart browser

---

#### Black screen / No video

**Solution:**
1. Check if camera is being used by another app
2. Close other video apps (Zoom, Teams, etc.)
3. Restart browser
4. Check Device Manager (Windows) for camera status
5. Try external webcam if available

---

#### No audio recording

**Solution:**
1. Check microphone permissions (same as camera)
2. Verify microphone works in other apps
3. Check browser console for errors
4. Try different browser

#### Error: "Failed to execute 'start' on 'MediaRecorder'"

**Solution:**
This is a browser compatibility issue. The app now automatically tries multiple audio formats:
1. Clear browser cache and reload
2. Update to latest Chrome/Edge version
3. Try Firefox as alternative
4. The app will use the best supported format automatically

---

### 🔴 Gemini API Issues

#### Error: "API key not valid"

**Solution:**
1. Verify API key is correct (no extra spaces)
2. Check if key is active at https://aistudio.google.com/
3. Try generating a new key
4. Ensure key has Gemini API access

---

#### Error: "Quota exceeded"

**Solution:**
1. Check quota at https://aistudio.google.com/
2. Wait for quota reset (usually daily)
3. Upgrade to paid tier if needed
4. Use different API key

---

#### Response: "System uncertain, try again"

**This is normal!** The AI only responds when confident (≥70%).

**To improve results:**
1. **Better lighting** - Ensure face/scene is well-lit
2. **Clearer audio** - Speak clearly, reduce background noise
3. **Specific intent** - Be more detailed in your intent text
4. **Relevant context** - Ensure camera shows relevant scene

**Example improvements:**
- ❌ "Help me" → ✅ "I'm preparing for a job interview"
- ❌ "Work" → ✅ "I'm trying to focus on writing a report"

---

### 🔴 Performance Issues

#### Slow response times (>5 seconds)

**Solution:**
1. Check internet connection speed
2. Reduce image size in `backend/config.py`:
   ```python
   MAX_IMAGE_SIZE_KB = 300  # Reduce from 500
   ```
3. Check Gemini API status
4. Verify no other heavy processes running

---

#### High CPU usage

**Solution:**
1. Close unnecessary browser tabs
2. Reduce video resolution in `frontend/src/App.jsx`:
   ```javascript
   video: { width: 640, height: 480 }  // Reduce from 1280x720
   ```
3. Check for memory leaks in browser console

---

### 🔴 Development Issues

#### Changes not reflecting

**Frontend:**
```bash
# Hard refresh
Ctrl + Shift + R (Windows)
Cmd + Shift + R (Mac)

# Or clear cache and restart dev server
```

**Backend:**
```bash
# Restart server
Ctrl + C
python main.py
```

---

#### Linting errors

**Solution:**
```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
pip install pylint
pylint main.py
```

---

### 🔴 Windows-Specific Issues

#### PowerShell execution policy error

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

#### Path issues with Python

**Solution:**
```bash
# Use full path
C:\Python310\python.exe main.py

# Or add Python to PATH
```

---

## 🔍 Debugging Tips

### Enable Verbose Logging

**Backend:**
```python
# In main.py, add at top
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// In App.jsx, add console logs
console.log('Image captured:', imageBase64.length);
console.log('Audio recorded:', audioBase64.length);
console.log('Response:', data);
```

---

### Check Backend Health

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{"status":"ok"}
```

---

### Test API Manually

```bash
# Using curl (requires base64 image/audio)
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "test",
    "image": "base64_string_here",
    "audio": "base64_string_here"
  }'
```

---

### Browser Console

**Open DevTools:**
- Windows: `F12` or `Ctrl + Shift + I`
- Mac: `Cmd + Option + I`

**Check for:**
- Red errors in Console tab
- Failed requests in Network tab
- Permission issues in Console

---

## 📞 Still Having Issues?

1. **Run setup verification:**
   ```bash
   cd backend
   python test_setup.py
   ```

2. **Check versions:**
   ```bash
   python --version  # Should be 3.10+
   node --version    # Should be 16+
   ```

3. **Review logs:**
   - Backend: Terminal where `python main.py` is running
   - Frontend: Browser DevTools Console
   - Network: Browser DevTools Network tab

4. **Try minimal test:**
   - Fresh browser window
   - Incognito/Private mode
   - Different browser entirely

5. **Check system requirements:**
   - Windows 10/11
   - 4GB+ RAM
   - Webcam + microphone
   - Internet connection

---

## 🎯 Quick Diagnosis

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Backend won't start | Missing API key | Set `GEMINI_API_KEY` |
| Frontend blank | Backend not running | Start backend first |
| Camera not working | Permissions | Allow in browser settings |
| "System uncertain" | Low confidence | Better lighting/audio |
| Slow responses | Network/API | Check internet speed |
| CORS errors | Wrong ports | Backend:8000, Frontend:5173 |

---

**Remember:** This is a hackathon MVP. If something doesn't work perfectly, that's okay! The goal is to demonstrate the concept, not production-grade reliability.
