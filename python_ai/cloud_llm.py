import sys, json, requests, os
from dotenv import load_dotenv

# Load local .env
load_dotenv() 

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

def generate_enterprise_audit(bpm, vibe, peaks_json, trends_json, lyrics_json):
    if not GROQ_API_KEY:
        error_msg = "CRITICAL: GROQ_API_KEY not found in Environment Secrets!"
        sys.stdout.write(json.dumps({"status": "error", "strategy": error_msg}))
        return

    try: 
        peaks_data = json.loads(peaks_json)
    except: 
        peaks_data = "Data corrupted"
    
    try: 
        trends_dict = json.loads(trends_json)
        live_genres = json.dumps(trends_dict.get("platforms", trends_dict))
    except: 
        live_genres = "Global Viral Data"
    
    try: 
        lyrics_data = json.loads(lyrics_json)
        lyrics = lyrics_data.get("lyrics", "No lyrics detected.")
    except: 
        lyrics = "No lyrics detected."

    # The Prompt Structure
    prompt = (
        f"ROLE: Visionary A&R Executive & Lead Data Scientist.\n\n"
        f"HARD DATA INPUTS:\n"
        f"- Tempo: {bpm} BPM\n"
        f"- Sonic Texture: {vibe}\n"
        f"- Transient Peaks (Hooks): {peaks_data}\n"
        f"- Lyrical Context: '{lyrics}'\n"
        f"- Global Market Behaviors: {live_genres}\n\n"
        f"TASK: Produce a brutally precise, highly formatted Executive A&R Strategy. NO fluff. NO generic music advice. You MUST cite the exact mathematical inputs above to justify every claim you make.\n\n"
        f"REQUIRED SECTIONS & FORMATTING:\n"
        f"### 📊 1. SONIC DNA & DEMOGRAPHIC MATCH\n"
        f"Analyze the BPM and Texture. Who is the exact target demographic? What specific commercial moods does this fit? (Use bullet points for quick scanning).\n\n"
        f"### 🗺️ 2. THE HOOK TIMELINE & VIRAL DROP\n"
        f"Review the Transient Peaks. Identify the 'Viral Drop' (the peak with the highest score). Explain exactly why this specific timestamp is the highest-converting moment for short-form content.\n\n"
        f"### 🚫 3. THE REJECTION PROTOCOL\n"
        f"List 2 global trends from the data that we MUST AVOID because they mathematically or culturally clash with the track, and explain why.\n\n"
        f"### 📱 4. SURGICAL CONTENT FUNNEL\n"
        f"Give precise video editing pacing based on the BPM (e.g., 'At {bpm} BPM, cuts must happen every X frames'). Specify exactly which timestamp to use for TikTok/Reels audio clips.\n\n"
        f"### 💰 5. SYNC & PLACEMENT TARGETS\n"
        f"Based on the Vibe and Lyrics, pitch 3 highly specific commercial licensing use-cases (e.g., 'A24 Psychological Thriller Trailer', 'Nike High-Intensity Ad', 'Late-night driving playlist')."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 3000,
        "temperature": 0.2 
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions", 
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"}, 
            json=payload,
            timeout=60 # Add timeout to prevent cloud hanging
        )
        
        res_json = response.json()
        
        if response.status_code == 200:
            if 'choices' in res_json:
                strategy = res_json['choices'][0]['message']['content']
            else:
                strategy = f"Unexpected API Response Format: {json.dumps(res_json)}"
        else:
            strategy = f"Groq API Error {response.status_code}: {res_json.get('error', {}).get('message', 'Unknown Error')}"
            
    except Exception as e:
        strategy = f"INTERNAL AUDIT ERROR: {str(e)}"

    # Output the final JSON for the Go Orchestrator
    sys.stdout.write(json.dumps({
        "status": "success", 
        "bpm": bpm, 
        "texture": vibe, 
        "lyrics": lyrics[:100]+"...", 
        "strategy": strategy
    }))

if __name__ == "__main__":
    if len(sys.argv) < 6: 
        sys.exit(1)
    generate_enterprise_audit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])