# DTMF Cipher App

Desktop and web application for encoding text into DTMF (Dual-Tone Multi-Frequency) signals and decoding them back.

## Features

- **Encode text to DTMF signals**: Convert any text (including Cyrillic) into DTMF symbol pairs and generate a WAV audio file
- **Decode DTMF signals**: Extract text from WAV files containing DTMF signals
- **Manual DTMF decoding**: Decode DTMF strings directly without audio files
- **Cross-platform**: Works as desktop app (Windows, macOS, Linux) and web app

## Installation

```bash
cd app/dtmf_cipher_app
pip install -r ../../requirements.txt
```

## Running the App

### Desktop App

```bash
flet run
```

### Web App

```bash
flet run --web
```

## Usage

### Encoding

1. Enter text in the input field or load from a file
2. Click "Generate WAV in memory" to convert to DTMF symbols
3. Click "Save/Download WAV" to generate an audio file with DTMF signals

### Decoding

#### From WAV file:
1. Select a WAV file containing DTMF signals
2. Click "Export Text to File" to save result to file

## Project Structure

```
app/dtmf_cipher_app/
├── src/
│   ├── main.py          # Flet application UI
│   ├── dtmf_core.py     # DTMF encoding/decoding logic
│   └── assets/          # App icons and splash screens
├── pyproject.toml
└── README.md
```

## Dependencies

- Python 3.12+
- flet >= 0.85.3
- numpy >= 2.5.1
- scipy >= 1.18.0

## How It Works

The app uses the Goertzel algorithm for DTMF frequency detection and standard DTMF frequency pairs:
- Low frequencies: 697, 770, 852, 941 Hz
- High frequencies: 1209, 1336, 1477, 1633 Hz

Each character is encoded as two frequency pairs and decoded using spectral analysis.
