from pathlib import Path
from typing import Optional
from mutagen import File

def get_audio_duration(file_path: Path) -> Optional[float]:
    try:
        audio_file = File(str(file_path))
        if audio_file is None:
            return None
        if hasattr(audio_file, 'info') and hasattr(audio_file.info, 'length'):
            return audio_file.info.length
        return None
    except Exception:
        return None

def format_duration(duration: float, format_type: str = 'mm-ss') -> str:
    if duration is None or duration < 0:
        return "00-00"
    
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    
    if format_type == 'mm-ss':
        return f"{minutes:02d}-{seconds:02d}"
    elif format_type == 'mm_ss':
        return f"{minutes:02d}_{seconds:02d}"
    elif format_type == 'ss':
        return f"{int(duration):03d}"
    else:
        return f"{minutes:02d}-{seconds:02d}"