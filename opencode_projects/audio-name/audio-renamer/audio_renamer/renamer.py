from pathlib import Path
from typing import List
from .duration import get_audio_duration, format_duration
from .scanner import scan_audio_files
from .config import Config

def generate_new_filename(old_file_path: Path, base_name: str, index: int, 
                          index_padding: int, time_format: str, separator: str) -> str:
    extension = old_file_path.suffix
    
    duration = get_audio_duration(old_file_path)
    if duration is None:
        duration = 0.0
    
    formatted_duration = format_duration(duration, time_format)
    
    padded_index = f"{index:0{index_padding}d}"
    
    new_filename = f"{base_name}-{padded_index}-{formatted_duration}{extension}"
    
    return new_filename

def rename_audio_files(directory: Path, config: Config) -> List[str]:
    audio_files = scan_audio_files(directory, config.extensions)
    
    renamed_files = []
    
    for i, file_path in enumerate(audio_files, start=config.start_index):
        new_filename = generate_new_filename(
            file_path, 
            config.base_name, 
            i, 
            config.index_padding, 
            config.time_format, 
            config.separator
        )
        
        new_path = file_path.parent / new_filename
        
        file_path.rename(new_path)
        renamed_files.append(str(new_path))
    
    return renamed_files