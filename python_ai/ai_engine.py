import sys, json, warnings, torch, librosa, numpy as np, os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging

# Hardware Optimization for M4
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
logging.set_verbosity_error()
warnings.filterwarnings("ignore")

def generate_global_strategy(peak_second, file_path):
    # Use Metal (MPS) for high-speed AI inference on M4
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # 'Listen' to the Local Audio DNA
    try:
        y, sr = librosa.load(file_path, duration=30)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = int(tempo[0]) if isinstance(tempo, np.ndarray) else int(tempo)
    except:
        bpm = 120

    # Read the 'Internet Training' Data
    try:
        with open("../trends.json", "r") as f:
            global_dna = json.load(f)
    except:
        global_dna = {"trending_bpms": "140", "viral_video_patterns": "Dynamic"}

    # Load the High-End Free Expert Model
    model_name = "google/flan-t5-base" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    # THE MASTER STRATEGIST PROMPT (Human-Like Reasoning)
    master_prompt = (
        f"Context: You are a World-Class Music Marketing Executive. "
        f"Global Trend Data: Viral BPMs are {global_dna['trending_bpms']}. "
        f"Current Viral Patterns: {global_dna['viral_video_patterns']}. "
        f"Client Song: {bpm} BPM. High energy hook found at {peak_second} seconds. "
        f"Task: Provide a deep, human-like viral execution plan. Explain exactly HOW to edit the video, "
        f"the emotional 'hook' to use, and why this specific BPM will beat the algorithm globally. "
        f"Detailed Global Strategy:"
    )

    inputs = tokenizer(master_prompt, return_tensors="pt").to(device)
    # Increased tokens for a full, detailed review
    outputs = model.generate(**inputs, max_new_tokens=450, do_sample=True, temperature=0.7)
    strategy = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Final Clean Output
    output_data = {
        "status": "success",
        "expert_analysis": {
            "bpm": bpm,
            "texture": "Global DNA Match",
            "strategy": strategy.strip()
        }
    }
    sys.stdout.write(json.dumps(output_data))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    generate_global_strategy(sys.argv[1], sys.argv[2])