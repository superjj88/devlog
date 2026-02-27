#!/usr/bin/env python3
"""
Test script to rename new audio files in tests directory to "SHORT" with duration
"""

import os
import sys
from pathlib import Path

# Add the audio_renamer module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'audio-renamer'))

from audio_renamer.duration import get_audio_duration, format_duration

def rename_new_audio_files():
    """Rename new audio files in tests directory to 'SHORT' with duration"""
    
    # Get the tests directory
    tests_dir = Path("./tests")
    
    # Check if tests directory exists
    if not tests_dir.exists():
        print("Error: Tests directory not found")
        return False
    
    # Supported audio extensions
    audio_extensions = ['.mp3', '.wav', '.flac']
    
    # Find all audio files
    audio_files = []
    for file in tests_dir.iterdir():
        if file.is_file() and file.suffix.lower() in audio_extensions:
            audio_files.append(file)
    
    # Sort files for consistent ordering
    audio_files.sort()
    
    print(f"Found {len(audio_files)} audio files to rename:")
    
    # Rename each file
    renamed_files = []
    for i, file_path in enumerate(audio_files, start=1):
        try:
            # Get duration
            duration = get_audio_duration(file_path)
            if duration is None:
                print(f"Warning: Could not get duration for {file_path.name}")
                continue
            
            # Format duration as mm_ss
            formatted_duration = format_duration(duration, "mm_ss")
            
            # Create new filename: background-{index}-{duration}.{extension}
            new_filename = f"background-{i:02d}-{formatted_duration}{file_path.suffix}"
            new_path = file_path.parent / new_filename
            
            # Rename the file
            file_path.rename(new_path)
            renamed_files.append(new_path)
            print(f"Renamed: {file_path.name} -> {new_filename}")
            
        except Exception as e:
            print(f"Error renaming {file_path.name}: {e}")
            continue
    
    print(f"\nSuccessfully renamed {len(renamed_files)} files")
    return True

if __name__ == "__main__":
    rename_new_audio_files()