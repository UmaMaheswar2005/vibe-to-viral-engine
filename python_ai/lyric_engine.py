import sys, json, requests, os, wave
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extract_lyrics(file_path):
    # Surgical Extraction: Create a 2-minute snippet to bypass 25MB limits
    snippet_path = os.path.join(os.path.dirname(__file__), "transcription_snippet.wav")
    try:
        with wave.open(file_path, 'rb') as infile:
            params = infile.getparams()
            n_frames = min(infile.getnframes(), 120 * infile.getframerate())
            frames = infile.readframes(n_frames)
            with wave.open(snippet_path, 'wb') as outfile:
                outfile.setparams(params)
                outfile.writeframes(frames)
    except:
        snippet_path = file_path # Fallback

    # Transcribe via Groq
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    try:
        with open(snippet_path, "rb") as f:
            files = {"file": ("snippet.wav", f, "audio/wav")}
            data = {"model": "whisper-large-v3"}
            response = requests.post(url, headers=headers, files=files, data=data)
            lyrics = response.json().get("text", "Instrumental or low-vocal track.")
    except:
        lyrics = "Lyric engine timeout."
    finally:
        # Clean up the temp file
        if os.path.exists(snippet_path) and snippet_path != file_path: 
            os.remove(snippet_path)

    sys.stdout.write(json.dumps({"status": "success", "lyrics": lyrics}))

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    extract_lyrics(sys.argv[1])