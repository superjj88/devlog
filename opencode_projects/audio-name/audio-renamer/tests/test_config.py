import tempfile
import os
from pathlib import Path
from audio_renamer.config import Config

def test_config_from_file():
    config_content = """
base_name: "Test_Audio"
start_index: 5
index_padding: 3
time_format: "mm:ss"
separator: " _ "
extensions:
  - mp3
  - wav
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name
    
    try:
        config = Config.from_file(Path(config_file))
        
        assert config.base_name == "Test_Audio"
        assert config.start_index == 5
        assert config.index_padding == 3
        assert config.time_format == "mm:ss"
        assert config.separator == " _ "
        assert config.extensions == ["mp3", "wav"]
    finally:
        os.unlink(config_file)

def test_config_default():
    config = Config.default_config()
    
    assert config.base_name == "Audio"
    assert config.start_index == 1
    assert config.index_padding == 2
    assert config.time_format == "mm-ss"
    assert config.separator == " - "
    assert config.extensions == ["mp3", "wav", "flac"]