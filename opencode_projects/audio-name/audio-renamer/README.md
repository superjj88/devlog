# Audio Folder Renamer

A CLI tool to rename audio files in a directory with duration information.

## Features

- Rename audio files with base name, index, and duration
- Support for multiple audio formats (mp3, wav, flac)
- Configurable naming patterns
- Command-line interface

## Installation

```bash
pip install .
```

## Usage

```bash
audio-renamer --dir /path/to/audio/files
```

## Configuration

Create a `config.yaml` file to customize the renaming behavior:

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

Then run:

```bash
audio-renamer --dir /path/to/audio/files --config config.yaml
```

## Example

Given an audio file `song.mp3`, the tool will rename it to something like:

```
Audio - 01 - 02-00.mp3
```

Where:
- `Audio` is the base name
- `01` is the file index (padded to 2 digits)
- `02-00` is the duration in minutes and seconds

## License

MIT