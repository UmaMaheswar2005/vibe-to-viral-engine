---
title: Vibe-to-Viral-Engine
emoji: 🎙️
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# 🎙️ Vibe-to-Viral: Enterprise A&R Audio Engine

An enterprise-grade, microservice-based audio analysis engine designed for A&R executives. It analyzes raw audio files using C++ digital signal processing, extracts sonic metadata (BPM, Texture), and leverages a Large Language Model to generate precise, data-driven viral marketing strategies.

## 🚀 Live Demo
**[Launch the Web Application on Hugging Face Spaces]**(https://huggingface.co/spaces/Mahi275/Vibe-to-Viral-Engine)

## 🧠 System Architecture

The system utilizes a polyglot microservice architecture for maximum performance and separation of concerns:

1. **Go API Gateway:** Acts as the central orchestrator, handling multipart file uploads, managing cross-origin requests, and routing data between microservices.
2. **C++ DSP Engine (`cpp_dsp`):** A high-performance transient detector built with CMake. It parses raw `.wav` byte streams to identify structural peaks and dynamic shifts in real-time.
3. **Python AI Ensemble (`python_ai`):** - **Audio Expert:** Extracts BPM, Spectral Centroid, and MFCC features using `librosa`.
   - **LLM Agent:** Integrates with the Groq API (Llama 3 70B) to generate cross-platform social media strategies based strictly on the extracted mathematical audio data.
4. **Streamlit Frontend:** A sleek, reactive dashboard for uploading tracks and viewing the generated enterprise audit.

## 🛠️ Local Installation & Development

This application is fully containerized. You do not need to install C++, Go, or Python locally to run it.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A free [Groq API Key](https://console.groq.com/keys) for the LLM features.

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UmaMaheswar2005/vibe-to-viral-engine.git
   cd vibe-to-viral-engine