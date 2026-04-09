import sys, json, warnings, librosa, numpy as np, os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
warnings.filterwarnings("ignore")

def extract_deep_audio_dna(file_path):
    try:
        y, sr = librosa.load(file_path, duration=30)
        
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = int(tempo[0]) if isinstance(tempo, np.ndarray) else int(tempo)
        
        # The Raw Math: We stop guessing and just send the science
        mfcc_mean = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)).item()
        contrast_mean = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr)).item()
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)).item()
        
        # We package the raw math as a string for the AI to interpret
        raw_science = f"Centroid: {int(centroid)}Hz | Contrast: {round(contrast_mean,2)}dB | MFCC: {round(mfcc_mean,2)}"

        sys.stdout.write(json.dumps({
            "status": "success",
            "bpm": bpm,
            "vibe_profile": raw_science # Passing math instead of words
        }))
        
    except Exception as e:
        sys.stdout.write(json.dumps({"status": "error", "bpm": 120, "vibe_profile": "Dynamic"}))

if __name__ == "__main__":
    extract_deep_audio_dna(sys.argv[1])