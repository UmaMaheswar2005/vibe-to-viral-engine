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
        f"ROLE: Visionary A&R Executive, Cultural Analyst, and Expert Music Producer.\n\n"
        f"CORE IDENTITY (THE SOUL):\n"
        f"- Lyrical Context & Emotion: '{lyrics}'\n"
        f"- Sonic Texture & Vibe: {vibe}\n\n"
        f"SUPPORTING MATH (THE SKELETON):\n"
        f"- Tempo: {bpm} BPM\n"
        f"- Transient Peaks (Hooks): {peaks_data}\n"
        f"- Global Market Behaviors: {live_genres}\n\n"
        f"CRITICAL GUARDRAILS:\n"
        f"1. EMOTION OVER MATH: The 'Soul' inputs dictate the genre, mood, and demographic. The 'Math' inputs ONLY dictate the video editing pacing. \n"
        f"2. THE BPM ILLUSION: Do NOT assume a tempo over 100 BPM means EDM, fitness, or high-energy pop. Many emotional, acoustic, and regional folk songs have fast tempos but melancholic or romantic vibes. \n"
        f"3. CULTURAL CONTEXT: Read the lyrics deeply. If they are romantic, devotional, or longing, your entire strategy MUST reflect human emotion. Never suggest 'sports,' 'fitness,' or 'energetic dance' for a lyrical ballad.\n\n"
        f"TASK: Produce a brutally precise, highly formatted Executive A&R Strategy. The lyrics must dictate the commercial placements, while the math must dictate the structural pacing.\n\n"
        f"REQUIRED SECTIONS & FORMATTING:\n"
        f"### 📊 1. SONIC DNA & DEMOGRAPHIC MATCH\n"
        f"Analyze the Soul and Skeleton. Who is the target demographic based on their *emotional* needs (e.g., seekers of nostalgia, romance, cultural connection)? What specific cinematic or intimate moods does this fit? (Use bullet points).\n\n"
        f"### 🗺️ 2. THE HOOK TIMELINE & VIRAL DROP\n"
        f"Identify the 'Viral Drop' (the peak with the highest score). Explain exactly why this timestamp connects emotionally with a listener.\n\n"
        f"### 🚫 3. THE REJECTION PROTOCOL\n"
        f"List 2 global trends that we MUST AVOID because they ruin the emotional or cultural integrity of this specific track.\n\n"
        f"### 📱 4. SURGICAL CONTENT FUNNEL\n"
        f"Give precise video editing pacing based on the {bpm} BPM. Specify exactly which timestamp to use for short-form video audio.\n\n"
        f"### 💰 5. SYNC & PLACEMENT TARGETS\n"
        f"Pitch 3 highly specific, emotionally resonant commercial licensing use-cases (e.g., 'Heartbreak montage in an Indie Film', 'Cultural documentary intro', 'Late-night acoustic playlist'). NO generic corporate ads unless the song is explicitly aggressive."
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