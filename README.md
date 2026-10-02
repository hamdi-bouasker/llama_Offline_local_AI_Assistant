# ⚡ Local AI Copilot: Real-Time Audio Transcription & Screen OCR

An ultra-fast, 100% private, and offline personal AI copilot running locally on your machine. This tool listens to active speaker audio (from meetings, streams, or calls) and captures on-screen text via hotkey, generating concise AI-driven responses using local LLMs.

---

## 🌟 Key Features

* **🎙️ Real-Time Audio Listening:** Uses `faster-whisper` on CPU (INT8 precision) to capture and transcribe speaker audio from video meetings or browser streams with Voice Activity Detection (VAD).
* **🖥️ On-Demand Screen OCR:** Press `Ctrl + Shift + S` to capture on-screen code, documents, or technical prompts instantly via `Tesseract OCR` without saving temporary files to disk.
* **🧠 100% Local Processing:** Routes all prompts through `Ollama` (`llama3.2:3b` or `llama3.1:8b`). Zero data leaves your machine.
* **⚡ VRAM Optimized:** Designed to run smoothly even on entry-level graphics cards (e.g., NVIDIA GTX 1060 4GB).

---

## 🏗️ System Architecture & Data Flow

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 580" width="100%" height="100%" style="background: #0d1117; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  <defs>
    <linearGradient id="audioGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0369a1" />
    </linearGradient>
    <linearGradient id="ocrGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9333ea" />
      <stop offset="100%" stop-color="#7e22ce" />
    </linearGradient>
    <linearGradient id="llmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16a34a" />
      <stop offset="100%" stop-color="#15803d" />
    </linearGradient>
    <linearGradient id="outGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c084fc" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#4ade80" />
    </marker>
  </defs>

  <rect x="15" y="15" width="870" height="550" rx="16" fill="#161b22" stroke="#30363d" stroke-width="2"/>

  <text x="450" y="50" fill="#f0f6fc" font-size="20" font-weight="700" text-anchor="middle">SYSTEM ARCHITECTURE &amp; DATA FLOW</text>
  <text x="450" y="72" fill="#8b949e" font-size="12" font-weight="400" text-anchor="middle">100% Offline Local Pipeline for Real-Time Audio Transcription and Screen OCR</text>

  <!-- LEFT COLUMN: AUDIO -->
  <rect x="50" y="105" width="230" height="60" rx="10" fill="#21262d" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="165" y="132" fill="#38bdf8" font-size="13" font-weight="600" text-anchor="middle">🎙️ Video Call / Meeting Audio</text>
  <text x="165" y="150" fill="#8b949e" font-size="11" text-anchor="middle">(Teams, Meet, Zoom, Browser)</text>

  <rect x="50" y="200" width="230" height="55" rx="10" fill="#1e293b" stroke="#0ea5e9" stroke-width="1.5"/>
  <text x="165" y="224" fill="#f0f6fc" font-size="12" font-weight="600" text-anchor="middle">VB-Audio Virtual Cable</text>
  <text x="165" y="241" fill="#38bdf8" font-size="10" text-anchor="middle">Software Loopback Driver</text>

  <rect x="50" y="290" width="230" height="65" rx="10" fill="url(#audioGrad)"/>
  <text x="165" y="317" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">faster-whisper (STT)</text>
  <text x="165" y="336" fill="#e0f2fe" font-size="11" text-anchor="middle">Runs on CPU • INT8 Precision</text>

  <!-- RIGHT COLUMN: OCR -->
  <rect x="620" y="105" width="230" height="60" rx="10" fill="#21262d" stroke="#c084fc" stroke-width="1.5"/>
  <text x="735" y="132" fill="#c084fc" font-size="13" font-weight="600" text-anchor="middle">🖥️ Active Screen / Workspace</text>
  <text x="735" y="150" fill="#8b949e" font-size="11" text-anchor="middle">(Browser, IDE, PDF, Code)</text>

  <rect x="620" y="200" width="230" height="55" rx="10" fill="#1e293b" stroke="#a855f7" stroke-width="1.5"/>
  <text x="735" y="224" fill="#f0f6fc" font-size="12" font-weight="600" text-anchor="middle">Keyboard Trigger</text>
  <text x="735" y="241" fill="#c084fc" font-size="11" font-weight="700" text-anchor="middle">[ Ctrl + Shift + S ]</text>

  <rect x="620" y="290" width="230" height="65" rx="10" fill="url(#ocrGrad)"/>
  <text x="735" y="317" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Tesseract OCR Engine</text>
  <text x="735" y="336" fill="#f3e8ff" font-size="11" text-anchor="middle">In-Memory Image Parsing</text>

  <!-- CENTER CORE: OLLAMA -->
  <rect x="310" y="380" width="280" height="80" rx="14" fill="url(#llmGrad)" stroke="#4ade80" stroke-width="2"/>
  <text x="450" y="412" fill="#ffffff" font-size="15" font-weight="700" text-anchor="middle">🧠 Local Ollama Engine</text>
  <text x="450" y="432" fill="#dcfce7" font-size="12" font-weight="600" text-anchor="middle">Endpoint: http://localhost:11434</text>
  <text x="450" y="449" fill="#bbf7d0" font-size="10" text-anchor="middle">Model: llama3.2:3b (4GB GPU) / llama3.1:8b (8GB+ GPU)</text>

  <!-- BOTTOM OUTPUT -->
  <rect x="220" y="490" width="460" height="55" rx="10" fill="url(#outGrad)" stroke="#30363d" stroke-width="1.5"/>
  <text x="450" y="513" fill="#4ade80" font-size="12" font-family="monospace" font-weight="600" text-anchor="middle">&gt; Terminal Console Stream Output</text>
  <text x="450" y="531" fill="#94a3b8" font-size="11" font-family="monospace" text-anchor="middle">Instant 3-Bullet Points | Concise Logic | 0ms Cloud Latency</text>

  <!-- FLOW ARROWS -->
  <line x1="165" y1="165" x2="165" y2="200" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <line x1="165" y1="255" x2="165" y2="290" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)"/>
  
  <line x1="735" y1="165" x2="735" y2="200" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)"/>
  <line x1="735" y1="255" x2="735" y2="290" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)"/>

  <path d="M 165 355 L 165 420 L 310 420" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-blue)"/>
  <path d="M 735 355 L 735 420 L 590 420" fill="none" stroke="#c084fc" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-purple)"/>

  <line x1="450" y1="460" x2="450" y2="490" stroke="#4ade80" stroke-width="2.5" marker-end="url(#arrow-green)"/>
</svg>

---

## 💡 Hardware & Model Recommendations

Choose the appropriate Ollama LLM based on your GPU's available VRAM:

| GPU Hardware | Recommended Model | Model Command | VRAM Usage |
| :--- | :--- | :--- | :--- |
| **Entry-Level** (4GB VRAM, e.g., GTX 1060 / 1650) | `llama3.2:3b` | `ollama run llama3.2:3b` | ~2.5 GB |
| **Mid-Range** (8GB VRAM, e.g., RTX 3060 / 4060) | `llama3.1:8b` | `ollama run llama3.1:8b` | ~5.2 GB |
| **High-End** (12GB+ VRAM, e.g., RTX 3080 / 4080) | `qwen2.5-coder:14b` | `ollama run qwen2.5-coder:14b` | ~9.0 GB |

---

## 🛠️ Prerequisites & Setup

### 1. External Requirements

* **[Python 3.10+](https://www.python.org/downloads/)** (Ensure **"Add python.exe to PATH"** is checked during setup).
* **[Ollama Engine](https://ollama.com/)** for running local LLMs.
* **[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)** (Installed path: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
* **[VB-Audio Virtual Cable](https://vb-audio.com/Cable/)** for routing system output audio to the script.

### 2. Audio Driver Configuration (Windows)

1. Press `Win + R`, type `mmsys.cpl`, and hit **Enter** to open Sound Control Panel.
2. **Playback Tab:** Right-click **CABLE Input (VB-Audio Virtual Cable)** and set as **Default Device**.
3. **Recording Tab:** Right-click **CABLE Output**, select **Properties** $\rightarrow$ **Listen** tab:
   * Check **"Listen to this device"**.
   * Under **Playback through this device**, select your physical **Headphones/Speakers**.

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone [https://github.com/your-username/local-ai-copilot.git](https://github.com/your-username/local-ai-copilot.git)
   cd local-ai-copilot
