# Qwen3-TTS Wrapper Documentation

## Architecture Overview

The Qwen3-TTS Wrapper is a voice assistant system that combines speech-to-text (STT), language model processing (LLM), and text-to-speech (TTS) capabilities. The system is designed to listen to user speech, transcribe it, process it through a language model, and respond with synthesized speech.

### Core Components

1. **STT (Speech-to-Text)**: `v1/stt.py`
   - Uses Faster-Whisper model for real-time speech recognition
   - Implements silence detection to automatically end recordings
   - Supports Hebrew and English languages

2. **LLM (Language Model)**: `v1/llm.py`
   - Uses Ollama to interface with Qwen3-8B model
   - Maintains chat history for context
   - Enforces English-only responses

3. **TTS (Text-to-Speech)**: `v1/daemon.py`
   - Uses Qwen3-TTS model for speech synthesis
   - Implements a daemon architecture for continuous listening
   - Handles audio playback through ALSA

4. **Pipeline**: `v1/pipeline.py`
   - Orchestrates the complete voice loop
   - Manages the flow from speech input to speech output
   - Includes noise filtering and hallucination detection

5. **GUI**: `v1/gui.py`
   - Provides a GTK-based graphical interface
   - Communicates with daemon via Unix socket
   - Offers start/stop toggle functionality

6. **Start Script**: `start.sh`
   - Manages the complete application lifecycle
   - Handles process cleanup and environment setup
   1. **STT (Speech-to-Text)**: `v1/stt.py`
   - Uses Faster-Whisper model for real-time speech recognition
   - Implements silence detection to automatically end recordings
   - Supports Hebrew and English languages

2. **LLM (Language Model)**: `v1/llm.py`
   - Uses Ollama to interface with Qwen3-8B model
   - Maintains chat history for context
   - Enforces English-only responses

3. **TTS (Text-to-Speech)**: `v1/daemon.py`
   - Uses Qwen3-TTS model for speech synthesis
   - Implements a daemon architecture for continuous listening
   - Handles audio playback through ALSA

4. **Pipeline**: `v1/pipeline.py`
   - Orchestrates the complete voice loop
   - Manages the flow from speech input to speech output
   - Includes noise filtering and hallucination detection

5. **GUI**: `v1/gui.py`
   - Provides a GTK-based graphical interface
   - Communicates with daemon via Unix socket
   - Offers start/stop toggle functionality

6. **Start Script**: `start.sh`
   - Manages the complete application lifecycle
   - Handles process cleanup and environment setup
   - Manages the complete application lifecycle
   - Handles process cleanup and environment setup
   - Implements silence detection to automatically end recordings
   - Supports Hebrew and English languages

2. **LLM (Language Model)**: `v1/llm (Copy).py`
   - Uses Ollama to interface with Qwen3-8B model
   - Maintains chat history for context
   - Enforces English-only responses

3. **TTS (Text-to-Speech)**: `v1/daemon (Copy).py`
   - Uses Qwen3-TTS model for speech synthesis
   - Implements a daemon architecture for continuous listening
   - Handles audio playback through ALSA

4. **Pipeline**: `v1/pipeline (Copy).py`
   - Orchestrates the complete voice loop
   - Manages the flow from speech input to speech output
   - Includes noise filtering and hallucination detection

5. **GUI**: `v1/gui (Copy).py`
   - Provides a GTK-based graphical interface
   - Communicates with daemon via Unix socket
   - Offers start/stop toggle functionality

6. **Start Script**: `start.sh`
   - Manages the complete application lifecycle
   - Handles process cleanup and environment setup

## Data Flow

The system follows this data flow:

```
User Speech → STT (Transcription) → LLM (Processing) → TTS (Synthesis) → User Speech
```

### Detailed Flow

1. **Recording Phase**
   - STT module records audio until silence is detected (2.5 seconds)
   - Minimum recording duration: 0.5 seconds
   - Silence threshold: 0.015 (adjustable)

2. **Transcription Phase**
   - Audio is processed by Whisper model
   - Text is extracted and cleaned
   - Hallucinations (false transcriptions) are filtered

3. **Processing Phase**
   - User text is sent to Qwen3-8B LLM
   - Response is generated in English
   - Chat history is maintained for context

4. **Synthesis Phase**
   - LLM response is sent to Qwen3-TTS model
   - Audio is generated with custom voice settings
   - Audio is played back through system speakers

5. **Loop Continuation**
   - System returns to recording phase
   - Process repeats continuously

## Module Descriptions

### STT Module (`v1/stt.py`)

**Purpose**: Convert spoken language to text

**Key Features**:
- Uses Faster-Whisper model (small size, float16 precision)
- Implements Voice Activity Detection (VAD)
- Configurable silence detection parameters
- Language support: Hebrew and English

**Main Functions**:
- `record_until_silence()`: Records audio until silence is detected
- `transcribe()`: Converts audio to text using Whisper

**Configuration**:
- `silence_threshold`: 0.015 (volume threshold for speech detection)
- `silence_duration`: 2.5 seconds (minimum silence to end recording)
- `min_recording_duration`: 0.5 seconds (minimum valid recording length)

### LLM Module (`v1/llm.py`)

**Purpose**: Process user input and generate responses

**Key Features**:
- Uses Ollama to interface with Qwen3-8B model
- Maintains conversation history
- Enforces English-only responses
- Character-limited to 8 billion parameters

**Main Functions**:
- `chat()`: Processes user input and returns LLM response

**Configuration**:
- `SYSTEM_PROMPT`: Defines assistant personality and language constraints
- Model: `qwen3:8b`

### TTS Module (`v1/daemon.py`)

**Purpose**: Convert text to speech and manage continuous listening

**Key Features**:
- Uses Qwen3-TTS model with custom voice support
- Implements daemon architecture for continuous operation
- Handles microphone input and audio playback
- Unix socket interface for remote control

**Main Classes**:
- `TTSDaemon`: Main daemon class with model loading and management

**Main Functions**:
- `load_models()`: Loads TTS and STT models
- `unload_models()`: Unloads models and cleans up memory
- `listen_until_silence()`: Records audio until silence detected
- `process_and_respond()`: Transcribes, processes, and synthesizes speech
- `start()`: Starts the listening daemon
- `stop()`: Stops the listening daemon
- `run_socket_server()`: Runs Unix socket server for remote control

**Configuration**:
- `MODEL_DIR`: `/mnt/storage/models/qwen3-tts`
- `TTS_MODEL_PATH`: `1.7B-CustomVoice`
- `SOCKET_PATH`: `/tmp/qwen3tts.sock`
- `SILENCE_THRESHOLD`: 0.02
- `SILENCE_DURATION`: 2.5 seconds

### Pipeline Module (`v1/pipeline.py`)

**Purpose**: Orchestrate the complete voice assistant workflow

**Key Features**:
- Manages the complete voice loop
- Implements noise and hallucination filtering
- Handles error recovery
- Provides clean interface for voice interactions

**Main Functions**:
- `speak()`: Generates and plays speech from text
- `voice_loop()`: Main application loop

**Configuration**:
- TTS speaker: `Ono_anna` (Japanese female voice)
- TTS instruct: Defines voice characteristics (cute, energetic, high pitch)
- Hallucinations list: Common false transcriptions to filter

### GUI Module (`v1/gui.py`)

**Purpose**: Provide graphical user interface for the voice assistant

**Key Features**:
- GTK 4.0 based interface
- Minimal window design
- Toggle button for start/stop functionality
- Status monitoring

**Main Classes**:
- `TTSWidget`: Main window widget
- `TTSApp`: GTK application class

**Main Functions**:
- `on_toggle()`: Handles toggle button state changes
- `check_status()`: Monitors daemon status
- `send_command()`: Communicates with daemon via socket

**Configuration**:
- Window size: 160x60 pixels
- Application ID: `dev.razik.qwen3tts`

## Usage Instructions

### Prerequisites

1. **Hardware Requirements**:
   - NVIDIA GPU with CUDA support (for model inference)
   - Microphone input device
   - Audio output device

2. **Software Requirements**:
   - Python 3.10+
   - CUDA Toolkit
   - ALSA (Advanced Linux Sound Architecture)
   - GTK 4.0

3. **Dependencies**:
   - torch
   - whisper
   - faster-whisper
   - sounddevice
   - numpy
   - soundfile
   - ollama
   - qwen_tts
   - gi (PyGObject)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
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
   ```

4. Download models:
   - Qwen3-TTS model (1.7B-CustomVoice)
   - Whisper small model
   - Qwen3-8B model for Ollama

### Running the Application

1. **Start the application**:
   ```bash
   ./start.sh
   ```

2. **Using the GUI**:
   - Click the toggle button to start/stop listening
   - Button label changes to indicate status:
     - "⏸ כבוי" (Off) - Not listening
     - "🎙️ מאזין..." (Listening) - Active

3. **Voice Interaction**:
   - Speak naturally when the system is listening
   - System will automatically detect silence and respond
   - Responses will be played through your audio output

4. **Stopping the application**:
   - Close the GUI window
   - Or press Ctrl+C in the terminal

### Command Line Usage

You can also run components individually:

1. **Run the daemon**:
   ```bash
   python v1/daemon.py
   ```

2. **Run the GUI**:
   ```bash
   python v1/gui.py
   ```

3. **Run the pipeline**:
   ```bash
   python v1/pipeline.py
   ```

## Configuration

### Model Configuration

**TTS Model**:
- Path: `/mnt/storage/models/qwen3-tts/1.7B-CustomVoice`
- Device: CUDA (automatically selected)
- Data type: bfloat16 for memory efficiency

**STT Model**:
- Model: Whisper small
- Device: CUDA
- Data type: float16

**LLM Model**:
- Model: Qwen3-8B
- Accessed via Ollama

### Audio Configuration

**Recording**:
- Sample rate: 16000 Hz
- Channels: 1 (mono)
- Data type: S16_LE (16-bit signed little-endian)
- Device: `hw:1,0` (UGREEN USB audio device)

**Playback**:
- Device: `hw:1,0` (UGREEN USB audio device)
- Format: WAV with PCM_16 subtype

### Silence Detection

**STT Module**:
- Silence threshold: 0.015
- Silence duration: 2.5 seconds
- Minimum recording duration: 0.5 seconds

**TTS Daemon**:
- Silence threshold: 0.02
- Silence duration: 2.5 seconds

### Voice Characteristics

**TTS Speaker**:
- Speaker: `Ono_anna` (Japanese female voice)
- Instruction: "A very cute, energetic, and sweet young anime girl voice, speaking enthusiastically with high pitch."

**LLM Personality**:
- Character: Cute, energetic anime girl
- Language: English only
- Response length: 1-3 sentences maximum

### Socket Communication

**Daemon Socket**:
- Path: `/tmp/qwen3tts.sock`
- Protocol: Unix domain socket
- Commands:
  - `{"action": "start"}`: Start listening
  - `{"action": "stop"}`: Stop listening
  - `{"action": "status"}`: Get current status

## Troubleshooting

### Common Issues

1. **Microphone not detected**:
   - Check ALSA device configuration
   - Verify microphone is connected and not muted
   - Try different device IDs in the recording command

2. **High VRAM usage**:
   - Models are automatically unloaded when stopped
   - Use `pkill -f "python.*daemon.py"` to force cleanup

3. **Audio playback issues**:
   - Ensure audio device is properly connected
   - Check volume levels and mute settings
   - Verify no other application is using the audio device

4. **Whisper transcription errors**:
   - Reduce silence threshold if recordings end too early
   - Increase silence duration if recordings are too long
   - Check for background noise affecting detection

5. **Ollama connection issues**:
   - Ensure Ollama service is running
   - Verify Qwen3-8B model is downloaded
   - Check network connectivity if using remote Ollama instance

### Debugging

1. **Check daemon logs**:
   ```bash
   cat /tmp/qwen3tts_daemon.log
   ```

2. **Run with verbose output**:
   ```bash
   python -u v1/daemon.py
   ```

3. **Test microphone**:
   ```bash
   arecord -D hw:1,0 -d 5 -f S16_LE -c 1 -r 16000 test.wav
   ```

4. **Test audio playback**:
   ```bash
   aplay test.wav
   ```

## Development Notes

### Code Structure

The codebase follows a modular design with clear separation of concerns:
- STT: Speech recognition
- LLM: Language processing
- TTS: Speech synthesis
- Pipeline: Workflow orchestration
- GUI: User interface
- Daemon: Background service

### Key Design Decisions

1. **Daemon Architecture**:
   - Separates background listening from user interface
   - Enables clean start/stop functionality
   - Allows remote control via Unix socket

2. **Silence Detection**:
   - Uses RMS (Root Mean Square) for volume calculation
   - Configurable thresholds for different environments
   - Minimum duration prevents false positives

3. **Hallucination Filtering**:
   - Common false transcriptions are filtered
   - Prevents system from responding to noise
   - Improves overall reliability

4. **Voice Characteristics**:
   - Custom instruction defines voice personality
   - Speaker selection provides consistent voice
   - Language enforcement ensures predictable behavior

### Future Improvements

1. **Multi-language support**: Extend beyond Hebrew and English
2. **Custom voice training**: Allow user-specific voice profiles
3. **Wake word detection**: Add keyword spotting for hands-free activation
4. **Batch processing**: Support for processing multiple audio files
5. **Remote access**: Web interface or network socket support

## License

This project is licensed under [MIT License]. See LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository.
