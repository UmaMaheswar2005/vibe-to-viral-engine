import sys, json, os, glob
import soundfile as sf
import numpy as np
import librosa

def log_message(message):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "splicer_log.txt")
    with open(log_path, "a") as f:
        f.write(message + "\n")

def ensemble_hook_detection(input_path, num_hooks=5):
    """
    The Master Engine: Combines 4 different MIR algorithms to find the ultimate hooks.
    """
    log_message("Initializing 4-Layer Ensemble Engine...")
    y, sr = librosa.load(input_path, sr=22050)
    
    # 1. Rhythm & Beat Drops (Onset)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_norm = librosa.util.normalize(onset_env)
    
    # 2. Chords & Key Changes (Chroma Flux)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_flux = np.sum(np.abs(np.diff(chroma, axis=1)), axis=0)
    chroma_flux = np.pad(chroma_flux, (1, 0), mode='constant')
    chroma_norm = librosa.util.normalize(chroma_flux)
    
    # 3. Vocals & Timbre Changes (MFCC Flux)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_flux = np.sum(np.abs(np.diff(mfcc, axis=1)), axis=0)
    mfcc_flux = np.pad(mfcc_flux, (1, 0), mode='constant')
    mfcc_norm = librosa.util.normalize(mfcc_flux)
    
    # 4. Pure Loudness (RMS)
    rms = librosa.feature.rms(y=y)[0]
    rms_norm = librosa.util.normalize(rms)
    
    # --- THE MASTER A&R SCORE ---
    # We weight rhythm and harmony the highest, ensuring we catch both rap and classical.
    master_score = (onset_norm * 0.4) + (chroma_norm * 0.3) + (mfcc_norm * 0.2) + (rms_norm * 0.1)
    
    # Find the peaks in the master score
    peaks = librosa.util.peak_pick(master_score, pre_max=15, post_max=15, pre_avg=15, post_avg=15, delta=0.15, wait=sr//512 * 10)
    times = librosa.frames_to_time(peaks, sr=sr)
    
    peak_intensities = master_score[peaks]
    sorted_indices = np.argsort(peak_intensities)[::-1]
    
    expert_hooks = []
    for idx in sorted_indices[:num_hooks]:
        sec = int(times[idx])
        expert_hooks.append({
            "time": f"{sec//60:02d}:{sec%60:02d}",
            "sec": sec,
            "val": float(peak_intensities[idx])
        })
        
    expert_hooks.sort(key=lambda x: x['sec'])
    return expert_hooks

def generate_clustered_previews(input_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Aggressive Cleanup
    for f in glob.glob(os.path.join(script_dir, "cluster_*.wav")):
        try: os.remove(f)
        except: pass
    hooks_file = os.path.join(script_dir, "final_hooks.json")
    if os.path.exists(hooks_file): os.remove(hooks_file)

    log_message(f"--- Processing: {os.path.basename(input_path)} ---")
    
    try:
        parsed_peaks = ensemble_hook_detection(input_path, num_hooks=8) # Grab more to allow for heavy filtering
        
        with open(hooks_file, "w") as f:
            json.dump(parsed_peaks, f)
            
        # Advanced Clustering
        clusters = []
        if parsed_peaks:
            current_cluster = [parsed_peaks[0]]
            for p in parsed_peaks[1:]:
                # Expand cluster window to 30 seconds
                if p['sec'] - current_cluster[0]['sec'] <= 30:
                    current_cluster.append(p)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [p]
            clusters.append(current_cluster)

        # Timbral Deduplication (The "Perfect Memory" Upgrade)
        data, samplerate = librosa.load(input_path, sr=22050)
        saved_count = 0
        fingerprints = [] # Will store 1D arrays of MFCC data

        for i, cluster in enumerate(clusters):
            start_sec = max(0, cluster[0]['sec'] - 1)
            duration_sec = 15 # Standard social media retention
            
            start_frame = int(start_sec * samplerate)
            end_frame = int((start_sec + duration_sec) * samplerate)
            
            if start_frame >= len(data): continue
            end_frame = min(end_frame, len(data))
            
            sliced_data = data[start_frame:end_frame]
            
            # Calculate MFCCs and average them over time to get a single 13-element signature
            mfcc = librosa.feature.mfcc(y=sliced_data, sr=samplerate, n_mfcc=13)
            fingerprint = np.mean(mfcc, axis=1) 
            
            is_duplicate = False
            for fp in fingerprints:
                # Calculate Cosine Similarity (How closely do the shapes of these vectors match?)
                similarity = np.dot(fingerprint, fp) / (np.linalg.norm(fingerprint) * np.linalg.norm(fp))
                
                # If it's 90% structurally similar, it's a repeated chorus/verse. We want to skip it to maximize variety.
                if similarity > 0.90:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                fingerprints.append(fingerprint)
                saved_count += 1
                output_path = os.path.join(script_dir, f"cluster_{saved_count}.wav")
                # Save using soundfile for best browser compatibility
                sf.write(output_path, sliced_data, samplerate, subtype='PCM_16')
                log_message(f"Saved Master Hook -> cluster_{saved_count}.wav")
            else:
                log_message(f"Skipped duplicate musical section for Cluster {i+1}")

        sys.stdout.write(json.dumps({"status": "success", "count": saved_count}))
        
    except Exception as e:
        log_message(f"FATAL ERROR: {str(e)}")
        sys.stdout.write(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    generate_clustered_previews(sys.argv[1])