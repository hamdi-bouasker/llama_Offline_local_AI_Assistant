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

![System Architecture]([https://github.com/hamdi-bouasker/llama_Offline_local_AI_Assistant/blob/master/Offline_AI_Assistant_System_Architecture.jpg])
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
