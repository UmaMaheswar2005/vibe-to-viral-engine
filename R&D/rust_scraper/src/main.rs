use serde::Serialize;
use std::fs::File;
use std::io::Write;

#[derive(Serialize)]
struct MarketMatrix {
    spotify_moods: Vec<String>,
    apple_global_charts: Vec<String>,
    tiktok_audio_meta: Vec<String>,
}

fn main() {
    let matrix = MarketMatrix {
        spotify_moods: vec!["Phonk".to_string(), "Deep House".to_string(), "Lo-Fi".to_string()],
        apple_global_charts: vec!["Global Hip-Hop".to_string(), "Telugu Pop".to_string()],
        tiktok_audio_meta: vec!["Beat Switches".to_string(), "140+ BPM Sprints".to_string()],
    };

    let j = serde_json::to_string_pretty(&matrix).unwrap();
    let mut file = File::create("../trends.json").unwrap();
    file.write_all(j.as_bytes()).unwrap();
    println!("✅ Rust Engine: Market Matrix Generated.");
}