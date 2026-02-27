import yaml
from pathlib import Path
from typing import List, Optional

class Config:
    def __init__(self, base_name: str, start_index: int, index_padding: int, 
                 time_format: str, separator: str, extensions: List[str]):
        self.base_name = base_name
        self.start_index = start_index
        self.index_padding = index_padding
        self.time_format = time_format
        self.separator = separator
        self.extensions = extensions

    @classmethod
    def from_file(cls, config_path: Path) -> 'Config':
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return cls(
            base_name=config_data.get('base_name', 'Audio'),
            start_index=config_data.get('start_index', 1),
            index_padding=config_data.get('index_padding', 2),
            time_format=config_data.get('time_format', 'mm-ss'),
            separator=config_data.get('separator', ' - '),
            extensions=config_data.get('extensions', ['mp3', 'wav', 'flac'])
        )

    @classmethod
    def default_config(cls) -> 'Config':
        return cls(
            base_name='Audio',
            start_index=1,
            index_padding=2,
            time_format='mm-ss',
            separator=' - ',
            extensions=['mp3', 'wav', 'flac']
        )