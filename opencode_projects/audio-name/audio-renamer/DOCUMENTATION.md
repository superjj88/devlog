# Audio Renamer - Official Documentation

## Overview

Audio Renamer is a command-line tool that renames audio files in a directory by adding duration information to their filenames. It's designed to help organize audio collections by automatically extracting audio duration and incorporating it into a configurable naming pattern.

## Features

- **Automatic Duration Extraction**: Extracts actual audio duration from MP3, WAV, and FLAC files using the mutagen library
- **Configurable Naming Patterns**: Customize base names, indexing, time formats, and separators
- **Multiple Audio Formats**: Supports MP3, WAV, and FLAC files
- **Robust Error Handling**: Graceful handling of file operations and error conditions
- **Directory Validation**: Prevents invalid directory paths and ensures proper operation

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/audio-renamer.git
cd audio-renamer

# Install the package
pip install .
```

### Install as a Global Package

```bash
pip install audio-renamer
```

## Usage

### Basic Usage

```bash
audio-renamer --dir /path/to/audio/files
```

### With Custom Configuration

```bash
audio-renamer --dir /path/to/audio/files --config config.yaml
```

### Command Line Options

| Option | Description | Required | Default |
|-------|-------------|----------|---------|
| `--dir` | Path to directory containing audio files | Yes | None |
| `--config` | Path to YAML configuration file | No | Uses default configuration |

## Configuration

### Default Configuration

If no configuration file is provided, the tool uses the following defaults:

```yaml
base_name: "Audio"
start_index: 1
index_padding: 2
time_format: "mm-ss"
separator: " - "
extensions:
  - mp3
  - wav
  - flac
```

### Configuration Options

| Option | Type | Description | Default |
|-------|------|-------------|---------|
| `base_name` | string | Base name for all renamed files | "Audio" |
| `start_index` | integer | Starting index number for files | 1 |
| `index_padding` | integer | Number of digits to pad index with | 2 |
| `time_format` | string | Format for displaying duration | "mm-ss" |
| `separator` | string | Separator between components | " - " |
| `extensions` | array | List of audio file extensions to process | ["mp3", "wav", "flac"] |

### Time Format Options

| Format | Example | Description |
|-------|---------|-------------|
| `mm-ss` | `02-30` | Minutes-seconds with dash separator |
| `mm:ss` | `02:30` | Minutes-seconds with colon separator |
| `ss` | `150` | Total seconds only |

## Examples

### Example 1: Basic Renaming

**Input:**
```
my-audio-directory/
  song1.mp3
  song2.mp3
  song3.mp3
```

**Command:**
```bash
audio-renamer --dir my-audio-directory
```

**Output:**
```
my-audio-directory/
  Audio - 01 - 02-30.mp3
  Audio - 02 - 04-15.mp3
  Audio - 03 - 03-45.mp3
```

### Example 2: Custom Configuration

**Configuration File (config.yaml):**
```yaml
base_name: "My_Music"
start_index: 10
index_padding: 3
time_format: "mm:ss"
separator: " _ "
extensions:
  - mp3
  - wav
```

**Command:**
```bash
audio-renamer --dir my-audio-directory --config config.yaml
```

**Output:**
```
my-audio-directory/
  My_Music _ 010 _ 02:30.mp3
  My_Music _ 011 _ 04:15.mp3
  My_Music _ 012 _ 03:45.mp3
```

## Technical Details

### Audio Duration Extraction

The tool uses the [mutagen](https://mutagen.readthedocs.io/) library to extract audio duration information. Mutagen supports various audio formats including:

- **MP3**: Extracts duration from MPEG audio files
- **WAV**: Extracts duration from WAV files
- **FLAC**: Extracts duration from FLAC files

The duration extraction is robust and handles various error conditions:
- Missing or corrupted audio files
- Unsupported audio formats
- Files without duration metadata

### Error Handling

The tool includes comprehensive error handling:

1. **Directory Validation**: Checks if the specified directory exists and is accessible
2. **File Operation Errors**: Handles file renaming errors gracefully
3. **Audio Parsing Errors**: Returns 00-00 for files that cannot be parsed
4. **Configuration Errors**: Validates configuration file format

### Performance Considerations

- The tool processes files sequentially for reliability
- Duration extraction is optimized for typical audio file sizes
- Memory usage is proportional to the number of files in the directory

## Development

### Project Structure

```
audio-renamer/
├── audio_renamer/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration handling
│   ├── duration.py     # Audio duration extraction
│   ├── renamer.py      # File renaming logic
│   └── scanner.py      # Audio file scanning
├── tests/
│   ├── test_config.py
│   ├── test_duration.py
│   ├── test_renamer.py
│   └── __init__.py
├── setup.py            # Package configuration
├── README.md           # Project documentation
└── requirements.txt   # Dependencies
```

### Dependencies

- `mutagen>=1.45.0`: Audio metadata handling
- `PyYAML>=5.4.0`: YAML configuration parsing

### Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_duration.py

# Run with verbose output
pytest tests/ -v
```

### Code Quality

The project follows Python best practices:
- Type hints for function signatures
- Comprehensive error handling
- Modular design with clear separation of concerns
- Unit tests for core functionality

## Troubleshooting

### Common Issues

#### No files were renamed

**Cause**: The directory may not contain any supported audio files.

**Solution**: Check that the directory contains files with the extensions specified in your configuration (default: mp3, wav, flac).

#### Duration shows as 00-00

**Cause**: The audio file may be corrupted or unsupported.

**Solution**: Verify that the file is a valid audio file and that mutagen supports the format.

#### Permission denied error

**Cause**: Insufficient permissions to read/write files in the directory.

**Solution**: Run the tool with appropriate permissions or use a different directory.

#### Configuration file not found

**Cause**: The specified configuration file path is incorrect.

**Solution**: Verify the path to your configuration file and ensure it exists.

### Debugging

Enable verbose output by running:

```bash
python -m audio_renamer.cli --dir /path/to/files --config config.yaml
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create your branch from `main`
2. **Write tests** for new features or bug fixes
3. **Update documentation** if your changes affect usage
4. **Submit a pull request** with clear description of changes

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests, please open an issue on the [GitHub repository](https://github.com/yourusername/audio-renamer).

## Changelog

### Version 0.1.0

- Initial release
- Audio duration extraction using mutagen
- Configurable naming patterns
- Support for MP3, WAV, and FLAC formats
- Basic error handling and validation

## Roadmap

Future enhancements may include:
- Recursive directory scanning
- Parallel processing for large directories
- Progress tracking and reporting
- Advanced configuration options
- Support for additional audio formats
