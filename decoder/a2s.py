import numpy as np
from scipy.io import wavfile

DTMF_MATRIX = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

LOW_FREQS = [697, 770, 852, 941]
HIGH_FREQS = [1209, 1336, 1477, 1633]

def goertzel(samples, target_freq, sample_rate):

    N = len(samples)
    k = int(0.5 + ((N * target_freq) / sample_rate))
    w = (2 * np.pi / N) * k
    cosine = np.cos(w)
    coeff = 2 * cosine

    s_prev = 0.0
    s_prev2 = 0.0

    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s

    power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2
    return power

def decode_dtmf_wav(filename, window_ms=40, threshold=1.5e8):

    sample_rate, data = wavfile.read(filename)

    if len(data.shape) > 1:
        data = data[:, 0]

    if data.dtype != np.int16:
        data = (data / np.max(np.abs(data)) * 32767).astype(np.int16)

    window_size = int(sample_rate * (window_ms / 1000.0))

    decoded_string = []
    last_char = None

    for i in range(0, len(data) - window_size, window_size):
        chunk = data[i:i + window_size]

        low_energies = [goertzel(chunk, f, sample_rate) for f in LOW_FREQS]
        high_energies = [goertzel(chunk, f, sample_rate) for f in HIGH_FREQS]

        max_low_idx = np.argmax(low_energies)
        max_high_idx = np.argmax(high_energies)

        max_low_power = low_energies[max_low_idx]
        max_high_power = high_energies[max_high_idx]

        if max_low_power > threshold and max_high_power > threshold:
            detected_low = LOW_FREQS[max_low_idx]
            detected_high = HIGH_FREQS[max_high_idx]

            current_char = DTMF_MATRIX.get((detected_low, detected_high))

            if current_char and current_char != last_char:
                decoded_string.append(current_char)
                last_char = current_char
        else:

            last_char = None

    return "".join(decoded_string)

# of = "./encoder/output/example.wav"
# print(decode_dtmf_wav(of))
