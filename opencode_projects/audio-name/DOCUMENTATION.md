# Music Duration Renamer

## Introduction

Music Duration Renamer is a command-line tool that renames music files to include their duration information. This makes it easier to organize and identify tracks by their length, which is particularly useful for creating playlists with specific timing requirements or for matching tracks to time-sensitive contexts.

## How It Works (High-Level)

When executed, the tool performs the following sequence:

1. Parses command-line arguments to determine the target directory
2. Reads configuration settings
3. Scans the directory for supported audio file formats
4. Extracts duration metadata from each file
5. Generates new filenames incorporating the duration
6. Renames each file according to the new naming scheme

## Installation & Requirements

### Requirements

- Python 3.6 or higher
- mutagen library (for audio metadata extraction)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/music-duration-renamer.git
   cd music-duration-renamer
   ```

2. Install the required dependencies:
   ```bash
   pip install mutagen
   ```

## Usage

### CLI Command Format

```bash
python cli.py <directory_path> [--config <config_path>]
```

### Arguments

- `<directory_path>`: Path to the directory containing music files to be renamed
- `--config <config_path>`: (Optional) Path to a custom configuration file

### Example Command

```bash
python cli.py /path/to/music --config /path/to/config.json
```

### Example Config File

```json
{
  "filename_format": "{original_name} - {duration}",
  "duration_format": "mm:ss",
  "supported_formats": ["mp3", "flac", "ogg", "wav"]
}
```

## Configuration File

### Fields

- `filename_format`: Format string for the new filename. Use `{original_name}` and `{duration}` as placeholders.
- `duration_format`: Format for the duration (e.g., "mm:ss", "hh:mm:ss").
- `supported_formats`: List of supported audio file formats.

### Defaults

- `filename_format`: "{original_name} - {duration}"
- `duration_format`: "mm:ss"
- `supported_formats`: ["mp3", "flac", "ogg", "wav"]

## Project Structure

```
music_duration_renamer/
├── __init__.py
├── cli.py
├── config.py
├── duration_extractor.py
├── file_renamer.py
├── file_scanner.py
├── utils.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_duration_extractor.py
    ├── test_file_renamer.py
    ├── test_file_scanner.py
    └── test_utils.py
```

### File and Module Explanations

1. **cli.py**: Entry point for the application, handles command-line argument parsing, and orchestrates the entire renaming process.
2. **config.py**: Defines default configuration settings and handles configuration file parsing.
3. **duration_extractor.py**: Contains logic for extracting duration from audio files using the mutagen library.
4. **file_renamer.py**: Generates new filenames based on duration information and implements filename formatting rules.
5. **file_scanner.py**: Scans directories for supported audio file formats and provides an interface for iterating through audio files.
6. **utils.py**: Contains utility functions used across modules.
7. **tests/ directory**: Contains unit tests for all modules, following the same structure as the main application.

## Core Logic Breakdown

### File Scanning

- `file_scanner.py` walks through the directory and identifies supported audio file formats.
- Returns a list of file paths for processing.

### Audio Duration Extraction

- `duration_extractor.py` determines the file format and uses the appropriate extraction method.
- Returns duration in a consistent format.

### Filename Generation

- `file_renamer.py` creates a new filename that preserves the original filename and inserts the duration information.
- Applies any formatting rules from the configuration.

### File Renaming

- Original files are renamed to the new filenames.
- Operations are performed atomically to prevent data loss.

## Testing

### Test Coverage

- Comprehensive unit tests for all modules.
- Integration tests for component interactions.
- Special cases including unsupported file formats, malformed audio files, and permission issues.

### Running Tests

```bash
python -m pytest tests/
```

## Limitations & Assumptions

### Intentional Limitations

- Focus on common audio formats only.
- Assumes generated filenames will fit within filesystem limits.
- Not designed for concurrent access scenarios.

### Edge Cases and Potential Issues

- Behavior may vary across different operating systems.
- Relies on accurate duration metadata in files.
- Not optimized for extremely large directories.
- Potential issues with files containing timezone-specific metadata.

## Future Improvements

- Support for additional audio file formats.
- Automatic handling of filename length limitations.
- Enhanced error recovery and user feedback.
- Parallel processing for improved performance with large directories