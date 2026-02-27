from pathlib import Path
from typing import List
import os

def scan_audio_files(directory: Path, extensions: List[str]) -> List[Path]:
    audio_files = []
    
    if not directory.exists() or not directory.is_dir():
        return audio_files
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix[1:].lower() in extensions:
            audio_files.append(file_path)
    
    audio_files.sort()
    return audio_files