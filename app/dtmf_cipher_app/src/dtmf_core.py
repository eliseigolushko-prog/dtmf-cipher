import io
import numpy as np
import scipy.io.wavfile as wavfile

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \nабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
EN_LIST = list("0123456789ABCD*#")
DTMF_FREQ = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1636),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1636),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1636),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1636)
}

LOW_FREQS = sorted(list({v[0] for v in DTMF_FREQ.values()}))
HIGH_FREQS = sorted(list({v[1] for v in DTMF_FREQ.values()}))
DTMF_MATRIX = {v: k for k, v in DTMF_FREQ.items()}

def read_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return str(f.read())

def text_to_dtmf_string(text: str) -> str:
    res = []
    for c in text:
        if c in CHARS:
            idx = CHARS.index(c)
            res.extend([EN_LIST[int(idx / 16)], EN_LIST[idx % 16]])
    return "".join(res)

def dtmf_string_to_text(dtmf_str: str) -> str:
    res = []
    for i in range(0, len(dtmf_str) - 1, 2):
        if dtmf_str[i] in EN_LIST and dtmf_str[i+1] in EN_LIST:
            idx = EN_LIST.index(dtmf_str[i]) * 16 + EN_LIST.index(dtmf_str[i+1])
            if idx < len(CHARS): res.append(CHARS[idx])
    return "".join(res)

def generate_wav_bytes(text: str, tone_ms=100, silence_ms=80, rate=8000) -> bytes:

    dtmf_str = text_to_dtmf_string(text)
    if not dtmf_str: raise ValueError("No valid chars")
    t = np.linspace(0, tone_ms/1000, int(rate * (tone_ms/1000)), endpoint=False)
    sil = np.zeros(int(rate * (silence_ms/1000)), dtype=np.int16)
    fade = int(rate * 0.005)
    w = np.ones_like(t); w[:fade] = np.linspace(0, 1, fade); w[-fade:] = np.linspace(1, 0, fade)
    chunks = []
    for c in dtmf_str:
        if c in DTMF_FREQ:
            f1, f2 = DTMF_FREQ[c]
            tone_signal = ((0.5*np.sin(2*np.pi*f1*t) + 0.5*np.sin(2*np.pi*f2*t)) * w * 32767).astype(np.int16)
            chunks.extend([tone_signal, sil])

    wav_io = io.BytesIO()
    wavfile.write(wav_io, rate, np.concatenate(chunks))
    return wav_io.getvalue()

def goertzel(samples, target, rate):
    N = len(samples)
    coeff = 2 * np.cos((2 * np.pi / N) * int(0.5 + ((N * target) / rate)))
    s1, s2 = 0.0, 0.0
    for s in samples: s0 = s + coeff * s1 - s2; s2, s1 = s1, s0
    return s2*s2 + s1*s1 - coeff*s1*s2

def decode_wav_bytes_to_text(file_bytes: bytes, win_ms=30, thres=1.2e8) -> tuple[str, str]:
    wav_io = io.BytesIO(file_bytes)
    rate, data = wavfile.read(wav_io)
    if len(data.shape) > 1: data = data[:, 0]
    if data.dtype != np.int16: data = (data / np.max(np.abs(data)) * 32767).astype(np.int16)
    w_size = int(rate * (win_ms / 1000))
    chars, last = [], None
    for i in range(0, len(data) - w_size, w_size):
        chunk = data[i:i + w_size]
        il = np.argmax([goertzel(chunk, f, rate) for f in LOW_FREQS])
        ih = np.argmax([goertzel(chunk, f, rate) for f in HIGH_FREQS])
        if goertzel(chunk, LOW_FREQS[il], rate) > thres and goertzel(chunk, HIGH_FREQS[ih], rate) > thres:
            cur = DTMF_MATRIX.get((LOW_FREQS[il], HIGH_FREQS[ih]))
            if cur and cur != last: chars.append(cur); last = cur
        else: last = None
    s = "".join(chars)
    return s, dtmf_string_to_text(s)
