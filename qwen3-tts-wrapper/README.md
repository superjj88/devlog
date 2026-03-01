# Qwen3-TTS Voice Assistant Wrapper

A real-time voice assistant system built with Qwen3-TTS, Whisper STT, and Ollama LLM integration.

## Overview

This project implements a full-duplex voice assistant that:
- Records audio from microphone until silence is detected
- Transcribes speech to text using Faster-Whisper (STT)
- Processes text with Qwen3 LLM
- Converts text back to speech using Qwen3-TTS (TTS)
- Plays the audio output in real-time

## Features

- **Real-time voice interaction**: Continuous listening with silence detection
- **Multi-language support**: Hebrew and English speech recognition
- **Secure architecture**: Input validation, rate limiting, and secure file handling
- **Unix socket interface**: Daemon mode with command control
- **GUI control panel**: Minimal GTK interface for start/stop control
- **Cross-platform compatibility**: Works on Linux systems with proper audio setup

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Voice Assistant System                   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Microphone │───▶│   STT (Whisper)│──▶│   LLM (Qwen3)│  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                      │                      │
│                                      ▼                      │
│                              ┌──────────────┐              │
│                              │   TTS (Qwen3)│              │
│                              └──────────────┘              │
│                                      │                      │
│                                      ▼                      │
│                              ┌──────────────┐              │
│                              │   Audio Out  │              │
│                              └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
src/
├── core/
│   ├── daemon.py          # Main daemon with socket interface
│   └── pipeline.py        # Audio processing pipeline
├── subsystems/
│   ├── stt.py             # Speech-to-text processing
│   └── llm.py             # Large language model integration
├── security/
│   ├── security_utils.py  # Input validation and sanitization
│   ├── rate_limiter.py    # Rate limiting implementation
│   └── temp_file_manager.py # Secure temporary file handling
├── utils/
│   ├── config.py          # Configuration management
│   └── logging_utils.py   # Logging utilities
└── ui/
    └── gui.py             # GTK-based GUI control panel
docs/
├── SECURITY.md            # Detailed security documentation
├── SECURITY_REPORT.md     # Security audit report
└── GITIGNORE_UPDATE_SUMMARY.md # Gitignore update summary
scripts/
└── start.sh               # Startup script for quick deployment
```

## Requirements

- Python 3.10+
- PyTorch with CUDA support
- Whisper (faster-whisper)
- Qwen3-TTS
- SoundDevice
- GTK 4.0 (for GUI)
- Ollama (for LLM integration)

See `requirements.txt` for full dependencies.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/qwen3-tts-wrapper.git
cd qwen3-tts-wrapper
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install faster-whisper torch soundfile numpy
```

4. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Ensure model files are in place:
- Qwen3-TTS model at `MODEL_DIR/1.7B-CustomVoice`
- Faster-Whisper model (large-v3-turbo)
- Ollama with Qwen3 model (qwen3:8b)

## Configuration

Edit `.env` with your settings:

```bash
# Model paths
MODEL_DIR=/mnt/storage/models/qwen3-tts
TTS_MODEL_PATH=${MODEL_DIR}/1.7B-CustomVoice

# Socket path
SOCKET_PATH=/tmp/qwen3tts.sock

# Temporary files
TEMP_PLAY_FILE=/tmp/qwen_play.wav

# Audio processing thresholds
SILENCE_THRESHOLD=0.02
SILENCE_DURATION=2.5

# Rate limiting (requests per minute)
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/qwen3tts.log

# Socket permissions (octal)
SOCKET_PERMISSIONS=0660
```

## Usage

### Quick Start

Run the startup script:
```bash
./scripts/start.sh
```

This will:
1. Start the daemon in background
2. Launch the GUI control panel
3. Automatically shut down daemon when GUI is closed

### Manual Start

1. Start the daemon:
```bash
python src/core/daemon.py
```

2. In another terminal, start the GUI:
```bash
python src/ui/gui.py
```

### Using the GUI

The GUI provides a minimal toggle button:
- **⏸ כבוי** (Off): Daemon is stopped
- **🎙️ מאזין...** (Listening...): Daemon is active and listening

The GUI automatically checks daemon status every 2 seconds.

### Socket Interface

The daemon exposes a Unix socket at `/tmp/qwen3tts.sock` for command control.

#### Commands

```json
{"action": "start"}   // Start listening
{"action": "stop"}    // Stop listening
{"action": "status"}  // Get current status
```

#### Example

```bash
# Start the daemon
python src/core/daemon.py &

# Check status
echo '{"action": "status"}' | nc -U /tmp/qwen3tts.sock

# Start listening
echo '{"action": "start"}' | nc -U /tmp/qwen3tts.sock

# Stop listening
echo '{"action": "stop"}' | nc -U /tmp/qwen3tts.sock
```

## Security Features

- **Input validation**: All user input is validated for length, content, and format
- **Sanitization**: Input is sanitized to prevent injection attacks
- **Rate limiting**: Prevents abuse via sliding window algorithm
- **Secure file handling**: Temporary files created with owner-only permissions
- **Unix socket permissions**: Configurable socket access control
- **Structured logging**: Security events logged separately
- **Sensitive data redaction**: Automatic redaction from logs

See `docs/SECURITY.md` for detailed security documentation.

## Audio Processing

### Silence Detection

The system uses RMS (Root Mean Square) volume calculation:
- **Threshold**: `SILENCE_THRESHOLD` (default: 0.02)
- **Duration**: `SILENCE_DURATION` (default: 2.5 seconds)

When volume falls below threshold for the specified duration, recording stops.

### Audio Format

- Input: 16-bit PCM, 16kHz, mono (raw format from arecord)
- Output: 16-bit PCM WAV file

## Troubleshooting

### Common Issues

1. **No audio input**: Check microphone permissions and device selection
2. **Model not found**: Verify `MODEL_DIR` and `TTS_MODEL_PATH` in `.env`
3. **CUDA out of memory**: Reduce batch size or use CPU mode
4. **Socket connection failed**: Verify socket path and permissions
5. **Ollama not running**: Ensure Ollama is running with the Qwen3 model

### Logs

Daemon logs are written to `/var/log/qwen3tts.log` (configurable via `LOG_FILE`).

## Version

v1.2.0

## License

This project follows the same license as the main Qwen3-TTS wrapper.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## Acknowledgements

- Qwen3-TTS team for the text-to-speech model
- OpenAI Whisper team for speech recognition
- Ollama team for LLM integration
- GTK team for GUI framework