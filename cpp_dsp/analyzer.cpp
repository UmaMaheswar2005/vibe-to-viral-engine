#define DR_WAV_IMPLEMENTATION
#include "dr_wav.h"
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

struct Peak {
    int second;
    float energy;
    std::string timestamp;
};

int main(int argc, char* argv[]) {
    if (argc < 2) return 1;
    unsigned int channels, sampleRate;
    drwav_uint64 totalFrames;
    float* pData = drwav_open_file_and_read_pcm_frames_f32(argv[1], &channels, &sampleRate, &totalFrames, NULL);
    if (!pData) return 1;

    std::vector<Peak> allPeaks;
    int windowSize = sampleRate * channels;
    float totalEnergy = 0;

    // First pass: Calculate average energy for thresholding
    for (drwav_uint64 i = 0; i < totalFrames * channels; i += windowSize) {
        float energy = 0.0f;
        int frames = (i + windowSize < totalFrames * channels) ? windowSize : (totalFrames * channels - i);
        for (int j = 0; j < frames; ++j) energy += pData[i + j] * pData[i + j];
        energy = std::sqrt(energy / frames);
        allPeaks.push_back({(int)(i / (sampleRate * channels)), energy, ""});
        totalEnergy += energy;
    }

    float avgEnergy = totalEnergy / allPeaks.size();
    std::vector<Peak> validPeaks;

    // Second pass: Identify "Significant Peaks" (1.5x louder than average)
    for (auto& p : allPeaks) {
        if (p.energy > avgEnergy * 1.5) {
            int mins = p.second / 60;
            int secs = p.second % 60;
            p.timestamp = (mins < 10 ? "0" : "") + std::to_string(mins) + ":" + (secs < 10 ? "0" : "") + std::to_string(secs);
            validPeaks.push_back(p);
        }
    }

    std::cout << "{\"status\":\"success\",\"peaks\":[";
    for(size_t i=0; i<validPeaks.size(); ++i) {
        std::cout << "{\"time\":\"" << validPeaks[i].timestamp << "\",\"val\":" << validPeaks[i].energy << "}" << (i < validPeaks.size()-1 ? "," : "");
    }
    std::cout << "]}";
    
    drwav_free(pData, NULL);
    return 0;
}