# DTMF Cipher

Tool for encoding text into DTMF (Dual-Tone Multi-Frequency) signals and decoding them back.

## Description

This project allows you to:
- Convert text into a sequence of DTMF codes
- Generate an audio file (`.wav`) containing DTMF signals
- Decode DTMF signals from audio files back into text

## Project Structure

```
├── app/              # Application of flet
│   └── dtmf_cipher_app/
│       ├── pyproject.toml
│       ├── README.md
│       └── src/
│           ├── dtmf_core.py  # DTMF core for app
│           ├── main.py       # Main file of app
│           └── assets/       # Icons
│               ├── icon.png
│               ├── icon.ico
│               └── favicon.png
├── encoder/           # Encoding module
│   ├── s2a.py        # Convert string to audio
│   ├── t2s.py        # Convert text to DTMF symbols
│   └── files/        # Input files
│       └── example.txt
│   └── output/       # Output .wav files
│       └── example.wav
├── decoder/           # Decoding module
│   ├── a2s.py        # Convert audio to string
│   ├── s2t.py        # Convert DTMF symbols to text
│   └── output/       # Output files
│       └── example.txt
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/eliseigolushko-prog/dtmf-cipher
cd dtmf-cipher
```
```bash
pip install -r requirements.txt
```

### Dependencies
- numpy==2.5.1
- scipy==1.18.0

## Usage

### Encoding text into DTMF signal

```bash
python encoder/s2a.py
```

The script reads `encoder/files/example.txt`, encodes it into a DTMF signal, and saves it to `encoder/output/example.wav`.

### Decoding DTMF signal to text

```bash
python decoder/s2t.py
```

The script reads `encoder/output/example.wav`, decodes the DTMF signal, and saves the result to `decoder/output/example.txt`.

### Decoding in web app

```bash
cd app/dtmf_cipher_app
flet run --web
```

### Creating application

```bash
cd app/dtmf_cipher_app
flet build macos # for macos
flet build windows # for windows
flet build linux # for linux
flet build apk # for android
flet build ipa # for ios
```

## DTMF Encoding

The project uses the following encoding scheme:
- Standard DTMF frequency set (4 low + 4 high frequencies)
- Symbols: `0-9`, `A-D`, `*`, `#`

## Example

Source text: `Hello, guys!`

1. Encoding → DTMF signal (`.wav`)
2. Decoding → Restored text

## Notes

- DTMF frequencies: 697, 770, 852, 941 Hz (low) and 1209, 1336, 1477, 1633 Hz (high)
- Default: tone duration 100 ms, silence duration 100 ms, sample rate 8000 Hz
- Smooth fade in/out is used for reliable signal recognition
