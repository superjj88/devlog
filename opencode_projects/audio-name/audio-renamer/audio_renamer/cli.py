import argparse
import sys
from pathlib import Path
from .config import Config
from .renamer import rename_audio_files

def main():
    parser = argparse.ArgumentParser(description='Rename audio files in a directory')
    parser.add_argument('--dir', required=True, help='Path to directory containing audio files')
    parser.add_argument('--config', help='Path to YAML configuration file')
    
    args = parser.parse_args()
    
    directory = Path(args.dir)
    
    # Validate directory
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)
    
    if args.config:
        config = Config.from_file(Path(args.config))
    else:
        config = Config.default_config()
    
    try:
        renamed_files = rename_audio_files(directory, config)
        print(f"Renamed {len(renamed_files)} files")
    except Exception as e:
        print(f"Error during renaming: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()