import json
import threading
import numpy as np
import pyaudio
import requests
import pytesseract
import keyboard
from PIL import ImageGrab
from faster_whisper import WhisperModel

# ==============================================================================
# CONFIGURATION
# ==============================================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# Path to local Tesseract OCR executable
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Local Speech-to-Text Model ("tiny.en", "base.en", or "small.en")
WHISPER_MODEL_SIZE = "base.en"

# Audio Recording Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 300      # Adjust if Teams audio volume is low
SILENCE_CHUNKS_LIMIT = 20    # ~1.2 seconds of silence signals end of turn

# Thread lock to prevent interleaved Ollama outputs if Audio & OCR trigger together
ollama_lock = threading.Lock()

# ==============================================================================
# INITIALIZATION
# ==============================================================================
print("[+] Loading local Whisper model into RAM/VRAM...")
# Runs on CPU using INT8 math to save VRAM for Ollama and prevent DLL errors
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")
print("[+] Whisper STT Ready.")

def get_virtual_cable_index(p):
    """Finds VB-Audio Cable input index automatically."""
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev.get("name", "").upper()
        if "CABLE" in name or "VIRTUAL" in name:
            if dev.get("maxInputChannels", 0) > 0:
                return i
    return -1

def query_ollama(prompt, source_tag="Audio"):
    """Streams responses from local Ollama endpoint."""
    with ollama_lock:
        system_instruction = (
            "You are an offline technical interview copilot. "
            "If the question is a coding problem, explain the optimal approach and give the concise solution logic."
            "If the question is about a technical concept, provide a clear and detailed explanation without exceeding 200 words or 5 short sentences illustrated as bullet points. "
        )
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"System: {system_instruction}\nUser Question: {prompt}\nAnswer:",
            "stream": True
        }
        
        print(f"\n[+] Answer ({source_tag}):")
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=15)
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    print(chunk.get("response", ""), end="", flush=True)
            print("\n" + "-"*50 + "\n")
        except Exception as e:
            print(f"\n[!] Ollama Error: Is Ollama server running? Details: {e}\n")

# ==============================================================================
# OCR SCREEN SCANNER WORKER
# ==============================================================================
def capture_and_ocr():
    """Captures active screen, extracts text via Tesseract, and sends to Ollama."""
    print("\n\n[+] Trigger detected! Capturing screen for OCR...")
    try:
        # Grab full screen (use bbox=(left, top, right, bottom) if cropping a region)
        screenshot = ImageGrab.grab()
        text = pytesseract.image_to_string(screenshot).strip()
        
        if not text:
            print("[!] No readable text found on screen.")
            return

        print("--------------------------------------------------")
        print(f"[+] Screen Text Extracted:\n{text[:200]}..." if len(text) > 200 else f"[+] Screen Text Extracted:\n{text}")
        print("--------------------------------------------------")
        
        query_ollama(text, source_tag="Screen OCR")
    except Exception as e:
        print(f"[!] OCR Error: {e}")

def run_hotkey_listener():
    """Listens for Ctrl+Shift+S in a background thread."""
    keyboard.add_hotkey('ctrl+shift+s', capture_and_ocr)
    keyboard.wait()

# ==============================================================================
# MAIN AUDIO RECORDING LOOP
# ==============================================================================
def main():
    # Start the hotkey listener on a background thread
    hotkey_thread = threading.Thread(target=run_hotkey_listener, daemon=True)
    hotkey_thread.start()

    p = pyaudio.PyAudio()
    cable_index = get_virtual_cable_index(p)
    
    if cable_index == -1:
        print("[!] Error: VB-Audio Cable not found. Check Windows sound settings.")
        return

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=cable_index,
        frames_per_buffer=CHUNK
    )

    print(f"\n==================================================")
    print(f"      Master Offline Copilot Active!              ")
    print(f" • Audio: Listening on VB-Cable Index [{cable_index}]")
    print(f" • Screen: Press 'Ctrl + Shift + S' for OCR       ")
    print(f"==================================================\n")
    
    frames = []
    is_recording = False
    silent_chunks = 0

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()

            # Voice Activity Detection (VAD) via amplitude threshold
            if amplitude > SILENCE_THRESHOLD:
                if not is_recording:
                    print("\n[+] Speech Detected: Listening...", end="", flush=True)
                    is_recording = True
                frames.append(data)
                silent_chunks = 0
            elif is_recording:
                frames.append(data)
                silent_chunks += 1
                
                # If silence persists, process the recorded audio phrase
                if silent_chunks > SILENCE_CHUNKS_LIMIT:
                    print(" [Processing local AI]")
                    
                    # Convert raw PCM bytes directly to float32 NumPy array (bypasses PyAV file decoding)
                    audio_bytes = b''.join(frames)
                    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

                    # 1. Local STT (Whisper)
                    segments, _ = whisper_model.transcribe(audio_np, beam_size=1)
                    text_transcript = " ".join([segment.text for segment in segments]).strip()
                    
                    if text_transcript:
                        print(f"\n[Transcript]: \"{text_transcript}\"")
                        # 2. Local LLM (Ollama)
                        query_ollama(text_transcript, source_tag="Audio")
                    else:
                        print("[!] No clear text transcribed.")

                    # Reset buffers for next turn
                    frames = []
                    is_recording = False
                    silent_chunks = 0

    except KeyboardInterrupt:
        print("\n[-] Master Copilot stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()