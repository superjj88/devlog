#!/usr/bin/env python3
import tempfile
import os
from pathlib import Path
from audio_renamer.config import Config
from audio_renamer.duration import format_duration
from audio_renamer.scanner import scan_audio_files
from audio_renamer.renamer import generate_new_filename

def test_basic_functionality():
    print("Testing basic audio renamer functionality...")
    
    config = Config.default_config()
    print(f"Default config: {config.base_name}, {config.start_index}")
    
    duration = format_duration(120.0)
    print(f"Duration formatting: 120.0s -> {duration}")
    
    old_file = Path("test.mp3")
    new_filename = generate_new_filename(old_file, "Audio", 1, 2, "mm-ss", " - ")
    print(f"Generated filename: {new_filename}")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_basic_functionality()