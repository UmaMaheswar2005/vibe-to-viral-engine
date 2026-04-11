import streamlit as st
import requests
import json
import os  
import glob
import time

# --- CONFIG ---
st.set_page_config(page_title="Yombo Vibe-to-Viral", page_icon="🎙️", layout="wide")

# API Gateway End Point
API_URL = "http://127.0.0.1:8080/optimize" 

st.title("🎙️ Yombo Vibe-to-Viral: Enterprise Audit")

uploaded_file = st.file_uploader("Upload Master Track (WAV)", type="wav")

if uploaded_file and st.button("Generate Executive Strategy"):
    with st.spinner("Executing Deep A&R Audit (Math + Cloud AI)..."):
        try:
            # Prepare the request
            files = {'track': (uploaded_file.name, uploaded_file.getvalue(), 'audio/wav')}
            headers = {'X-API-Key': 'Client-Secret-Key-7742'}
            
            # Add a timeout to prevent the 'hanging' UI on cloud servers
            response = requests.post(API_URL, files=files, headers=headers, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                st.success("Enterprise Analysis Complete!")
                time.sleep(1.5)
                
                math = data.get('math_analysis') or {}
                ai_kit = data.get('ai_growth_kit') or {}
                expert = ai_kit.get('expert_analysis') or {}

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📈 Peak Transients (Hooks)")
                    st.write("**Listen to the Hook Clusters:**")
                    
                    # Target output directory
                    target_dir = "/app/python_ai"
                    
                    # Buffer for disk I/O
                    time.sleep(1.5) 
                    
                    cluster_files = sorted(glob.glob("/app/python_ai/cluster_*.wav"))
                    
                    if cluster_files:
                        for idx, c_file in enumerate(cluster_files):
                            with open(c_file, "rb") as f:
                                audio_bytes = f.read()
                                st.audio(audio_bytes, format="audio/wav")
                            st.caption(f"🎧 Hook Cluster #{idx+1}")
                    else:
                        st.warning("No audio clusters found. The engine is still generating them or the path is locked.")
                    
                    st.divider()
                    
                    st.write("**Full Ensemble Hook Map:**")
                    hooks_file_path = os.path.join(target_dir, "final_hooks.json")
                    
                    if os.path.exists(hooks_file_path):
                        with open(hooks_file_path, "r") as f:
                            final_hooks = json.load(f)
                        
                        if final_hooks:
                            for idx, p in enumerate(final_hooks):
                                # Using a more professional display for hooks
                                st.info(f"📍 Master Hook #{idx+1} found at {p.get('sec', 0)}s | Score: {round(p.get('val', 0), 2)}")
                        else:
                            st.write("No distinct peaks detected.")
                    else:
                        st.write("Awaiting hook calculation...")

                with col2:
                    st.subheader("🎵 Deep Sonic DNA")
                    # Displaying core metrics in a clean way
                    st.metric("Estimated Tempo", f"{expert.get('bpm', 'Analyzing...')} BPM")
                    st.write(f"**Vibe Texture:** {expert.get('texture', 'Analyzing...')}")

                st.divider()
                st.subheader("🎙️ Executive A&R Audit")
                st.markdown(expert.get('strategy', "Backend Error: The Cloud AI returned an empty response."))
            
            else:
                st.error(f"Gateway Error ({response.status_code}): {response.text}")

        except Exception as e:
            st.error(f"Connection failed: {e}")