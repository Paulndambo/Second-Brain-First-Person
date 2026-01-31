import { useState, useRef } from 'react'
import './App.css'

function App() {
  const [intent, setIntent] = useState('')
  const [status, setStatus] = useState('idle') // idle, observing, thinking, result
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const streamRef = useRef(null)
  
  const [cameraReady, setCameraReady] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderSupported = typeof MediaRecorder !== 'undefined'

  // Initialize camera
  const initCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: true
      })
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        streamRef.current = stream
        setCameraReady(true)
      }
    } catch (err) {
      setError('Camera/microphone access denied. Please allow permissions.')
      console.error('Media access error:', err)
    }
  }

  // Capture frame from video
  const captureFrame = () => {
    if (!canvasRef.current || !videoRef.current) return null
    
    const canvas = canvasRef.current
    const video = videoRef.current
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0)
    
    // Convert to base64 JPEG
    return canvas.toDataURL('image/jpeg', 0.85)
  }

  // Record audio
  const recordAudio = () => {
    return new Promise((resolve, reject) => {
      if (typeof MediaRecorder === 'undefined') {
        reject(new Error('MediaRecorder is not supported in this browser'))
        return
      }
      if (!streamRef.current) {
        reject(new Error('No media stream available'))
        return
      }

      audioChunksRef.current = []
      
      // Try different MIME types for browser compatibility
      let options = { mimeType: '' }
      const mimeTypes = [
        'audio/webm',
        'audio/webm;codecs=opus',
        'audio/ogg;codecs=opus',
        'audio/mp4',
        ''  // Let browser choose
      ]
      
      for (const mimeType of mimeTypes) {
        if (mimeType === '' || MediaRecorder.isTypeSupported(mimeType)) {
          options = mimeType ? { mimeType } : {}
          break
        }
      }
      
      const audioTracks = streamRef.current.getAudioTracks()
      if (!audioTracks || audioTracks.length === 0) {
        reject(new Error('No audio track available'))
        return
      }

      const audioStream = new MediaStream(audioTracks)

      let mediaRecorder
      try {
        mediaRecorder = new MediaRecorder(audioStream, options)
      } catch (err) {
        reject(new Error(`MediaRecorder creation failed: ${err.message}`))
        return
      }
      
      mediaRecorderRef.current = mediaRecorder

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const mimeType = mediaRecorder.mimeType || 'audio/webm'
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType })
        
        // Convert to base64
        const reader = new FileReader()
        reader.onloadend = () => {
          resolve(reader.result)
        }
        reader.onerror = reject
        reader.readAsDataURL(audioBlob)
      }

      mediaRecorder.onerror = (event) => {
        reject(new Error(`Recording error: ${event.error}`))
      }

      try {
        mediaRecorder.start()
        setIsRecording(true)

        // Record for 3 seconds
        setTimeout(() => {
          if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop()
            setIsRecording(false)
          }
        }, 3000)
      } catch (err) {
        reject(new Error(`Failed to start recording: ${err.message}`))
      }
    })
  }

  // Main analyze function
  const handleAnalyze = async () => {
    if (!intent.trim()) {
      setError('Please enter your intent')
      return
    }

    if (!cameraReady) {
      setError('Camera not ready')
      return
    }

    try {
      setError(null)
      setResult(null)
      setStatus('observing')

      // Capture image
      const imageBase64 = captureFrame()
      if (!imageBase64) {
        throw new Error('Failed to capture image')
      }

      // Record audio
      const audioBase64 = await recordAudio()

      setStatus('thinking')

      // Call backend
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          intent: intent,
          image: imageBase64,
          audio: audioBase64
        })
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
      setStatus('result')

    } catch (err) {
      setError(err.message || 'Analysis failed')
      setStatus('idle')
      console.error('Analysis error:', err)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Second Brain, First Person</h1>
        <p className="subtitle">Real-time multimodal cognitive assistant</p>
      </header>

      <main>
        {/* Video Preview */}
        <div className="video-container">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="video-preview"
          />
          <canvas ref={canvasRef} style={{ display: 'none' }} />
          
          {!cameraReady && (
            <div className="camera-overlay">
              <button onClick={initCamera} className="btn-primary">
                Enable Camera & Microphone
              </button>
            </div>
          )}
          
          {!mediaRecorderSupported && (
            <div className="error-message">
              Audio recording isn&apos;t supported in this browser. Please use a
              modern Chromium-based browser (Chrome, Edge).
            </div>
          )}

          {isRecording && (
            <div className="recording-indicator">
              <span className="pulse"></span> Recording...
            </div>
          )}
        </div>

        {/* Intent Input */}
        <div className="input-section">
          <input
            type="text"
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
            placeholder="What are you trying to accomplish?"
            className="intent-input"
            disabled={status === 'observing' || status === 'thinking'}
          />
          
          <button
            onClick={handleAnalyze}
            disabled={!cameraReady || status === 'observing' || status === 'thinking'}
            className="btn-analyze"
          >
            {status === 'observing' && 'Observing...'}
            {status === 'thinking' && 'Thinking...'}
            {(status === 'idle' || status === 'result') && 'Analyze'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Result Display */}
        {status === 'result' && result && (
          <div className="result-container">
            {result.intervention_needed ? (
              <div className="insight-card">
                <div className="insight-header">
                  <h2>💡 Insight</h2>
                  <span className="confidence">
                    {Math.round(result.confidence * 100)}% confident
                  </span>
                </div>
                
                <div className="insight-content">
                  <div className="insight-section">
                    <h3>Goal Detected</h3>
                    <p>{result.inferred_goal}</p>
                  </div>
                  
                  <div className="insight-section highlight">
                    <h3>Observation</h3>
                    <p>{result.insight}</p>
                  </div>
                  
                  <div className="insight-section">
                    <h3>Suggested Action</h3>
                    <p>{result.suggested_action}</p>
                  </div>
                  
                  <div className="insight-section">
                    <h3>Why It Matters</h3>
                    <p>{result.why_it_matters}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="no-insight">
                <p>✓ Everything looks good. No intervention needed.</p>
                {result.why_it_matters && (
                  <p className="system-note">{result.why_it_matters}</p>
                )}
              </div>
            )}
          </div>
        )}
      </main>

      <footer>
        <p>Powered by Gemini 3 API</p>
      </footer>
    </div>
  )
}

export default App
