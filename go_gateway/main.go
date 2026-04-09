package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

const ClientSecretKey = "Client-Secret-Key-7742"

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("X-API-Key") != ClientSecretKey {
			http.Error(w, `{"error": "Unauthorized"}`, http.StatusUnauthorized)
			return
		}
		next(w, r)
	}
}

func extractJSON(output []byte) string {
	str := string(output)
	start := strings.Index(str, "{")
	end := strings.LastIndex(str, "}")
	if start != -1 && end != -1 && start < end {
		return str[start : end+1]
	}
	return "{}"
}

func optimizeTrackHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

    if r.Method == "OPTIONS" {
        w.WriteHeader(http.StatusOK)
        return
    }

    r.ParseMultipartForm(50 << 20)
    file, _, err := r.FormFile("track")
    if err != nil {
        http.Error(w, "File upload error", http.StatusBadRequest)
        return
    }
    defer file.Close()

    tempFile, _ := os.CreateTemp("", "upload-*.wav")
    tempPath := tempFile.Name()
    defer os.Remove(tempPath)
    io.Copy(tempFile, file)
    tempFile.Close()

    var pythonExec string
    var rootPath string

    // Resolve execution environment
    if info, err := os.Stat("/app"); err == nil && info.IsDir() {
        pythonExec = "python3" 
        rootPath = "/app"
        fmt.Println("🐳 DOCKER MODE DETECTED")
    } else {
        // This is your local path
        pythonExec = "/Users/umamaheswarreddy/Documents/all_projects/music_project/python_ai/venv/bin/python3"
        rootPath = ".." 
        fmt.Println("💻 LOCAL MAC MODE DETECTED")
    }

    fmt.Printf("🐍 Final Interpreter Choice: %s\n", pythonExec)

    // C++ Engine
    cppBinaryPath := fmt.Sprintf("%s/cpp_dsp/build/analyzer", rootPath)
    cppOutput, _ := exec.Command(cppBinaryPath, tempPath).CombinedOutput()
    var cppData map[string]interface{}
    json.Unmarshal([]byte(extractJSON(cppOutput)), &cppData)
    
    // Audio Preview Splicer (Ensemble Engine)
    fmt.Println("🎬 Running 4-Layer Ensemble Hook Engine...")
    splicerScript := fmt.Sprintf("%s/python_ai/audio_splicer.py", rootPath)
    splicerCmd := exec.Command(pythonExec, splicerScript, tempPath)
    splicerCmd.Dir = fmt.Sprintf("%s/python_ai", rootPath) // Set Working Dir so it saves files correctly
    splicerOut, err := splicerCmd.CombinedOutput()
    if err != nil {
        fmt.Printf("❌ Splicer Failed: %v\nOutput: %s\n", err, string(splicerOut))
    }

    // Audio Expert Service
    audioScript := fmt.Sprintf("%s/python_ai/audio_expert.py", rootPath)
    audioCmd := exec.Command(pythonExec, audioScript, tempPath)
    audioCmd.Dir = fmt.Sprintf("%s/python_ai", rootPath)
    audioOutput, _ := audioCmd.CombinedOutput()
    var audioData map[string]interface{}
    json.Unmarshal([]byte(extractJSON(audioOutput)), &audioData)
    
    bpm := fmt.Sprintf("%v", audioData["bpm"])
    vibe := fmt.Sprintf("%v", audioData["vibe_profile"])

    // Cloud Trend & Lyric Engines
    trendScript := fmt.Sprintf("%s/python_ai/cloud_trends.py", rootPath)
    trendCmd := exec.Command(pythonExec, trendScript)
    trendCmd.Dir = fmt.Sprintf("%s/python_ai", rootPath)
    trendOutput, _ := trendCmd.CombinedOutput()

    lyricScript := fmt.Sprintf("%s/python_ai/lyric_engine.py", rootPath)
    lyricCmd := exec.Command(pythonExec, lyricScript, tempPath)
    lyricCmd.Dir = fmt.Sprintf("%s/python_ai", rootPath)
    lyricOutput, _ := lyricCmd.CombinedOutput()
    
    trendJSON := extractJSON(trendOutput)
    lyricJSON := extractJSON(lyricOutput)

    // Cloud LLM Service
   hooksFilePath := fmt.Sprintf("%s/python_ai/final_hooks.json", rootPath)
    hooksBytes, err := os.ReadFile(hooksFilePath)
    
    // If it successfully read the file, use the real data. Otherwise, fallback to "[]" to prevent crashes in the LLM layer.
    hooksStr := "[]"
    if err == nil && len(hooksBytes) > 0 {
        hooksStr = string(hooksBytes)
    }

    // Pass the real hooksStr to the AI!
    llmScript := fmt.Sprintf("%s/python_ai/cloud_llm.py", rootPath)
    llmCmd := exec.Command(pythonExec, llmScript, bpm, vibe, hooksStr, trendJSON, lyricJSON)
    llmCmd.Dir = fmt.Sprintf("%s/python_ai", rootPath)
    llmOutput, _ := llmCmd.CombinedOutput()
    
    var finalAIData map[string]interface{}
    json.Unmarshal([]byte(extractJSON(llmOutput)), &finalAIData)

    finalResponse := map[string]interface{}{
        "math_analysis": cppData,
        "ai_growth_kit": map[string]interface{}{"expert_analysis": finalAIData},
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(finalResponse)
}

func main() {
	http.HandleFunc("/optimize", authMiddleware(optimizeTrackHandler))
	fmt.Println("🚀 Enterprise Gateway running on :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}