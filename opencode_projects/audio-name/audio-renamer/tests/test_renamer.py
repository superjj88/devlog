from pathlib import Path
from audio_renamer.renamer import generate_new_filename

def test_generate_new_filename():
    old_file = Path("test.mp3")
    
    # Test with a file that doesn't exist (should return 00-00)
    result = generate_new_filename(
        old_file, 
        "My_Audio", 
        1, 
        2, 
        "mm-ss", 
        " - "
    )
    
    assert result == "My_Audio - 01 - 00-00.mp3"
    
    result = generate_new_filename(
        old_file, 
        "Audio", 
        5, 
        3, 
        "mm:ss", 
        " _ "
    )
    
    assert result == "Audio _ 005 _ 00:00.mp3"