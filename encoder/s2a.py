import numpy as np
from scipy.io import wavfile
from t2s import read_file, encode
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def generate_robust_dtmf(dial_string: str, tone_ms: int = 100, silence_ms: int = 100, sample_rate: int = 8000) -> np.ndarray:
    """
    Генерирует идеальный DTMF-сигнал для онлайн-декодеров.
    tone_ms=100 (длительность звука) и silence_ms=100 (длительность тишины)
    гарантируют успешное распознавание алгоритмами.
    """
    dtmf_freqs = {
        '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1636),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1636),
        '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1636),
        '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1636)
    }

    # Переводим миллисекунды в секунды
    t_tone = np.linspace(0, tone_ms / 1000.0, int(sample_rate * (tone_ms / 1000.0)), endpoint=False)
    silence_signal = np.zeros(int(sample_rate * (silence_ms / 1000.0)), dtype=np.int16)

    # Создаем эффект плавного нарастания и затухания (Fade In / Fade Out),
    # чтобы убрать щелчки, которые сбивают с толку декодеры
    fade_len = int(sample_rate * 0.005)  # 5 миллисекунд на сглаживание углов
    window = np.ones_like(t_tone)
    window[:fade_len] = np.linspace(0, 1, fade_len)
    window[-fade_len:] = np.linspace(1, 0, fade_len)

    audio_chunks = []

    for char in str(dial_string).upper():
        if char in dtmf_freqs:
            f1, f2 = dtmf_freqs[char]

            # Синтезируем две частоты (амплитуда 0.5 + 0.5 = 1.0)
            tone = 0.5 * np.sin(2 * np.pi * f1 * t_tone) + 0.5 * np.sin(2 * np.pi * f2 * t_tone)

            # Применяем сглаживание и переводим в формат 16-бит PCM (-32768 до 32767)
            tone_int16 = ((tone * window) * 32767.0).astype(np.int16)

            audio_chunks.append(tone_int16)
            audio_chunks.append(silence_signal)  # Пауза после каждой цифры

    if not audio_chunks:
        raise ValueError("В строке не найдено валидных символов DTMF")

    return np.concatenate(audio_chunks)

fd = BASE_DIR / "files" / "example.txt" # you can insert any path here

f = read_file(fd)
ef = encode(f)

sef = ''.join(e for e in ef)
audio_data = generate_robust_dtmf(sef, tone_ms=100, silence_ms=100)

of = BASE_DIR / "output" / "example.wav" # you can insert any path here
sample_rate = 8000

wavfile.write(of, sample_rate, audio_data)
print(f"File {of} had been saved succesfully!")
