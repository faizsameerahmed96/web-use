import pyaudio
import wave
import numpy as np
from audio.transcription import transcribe_audio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "temp_output/output.wav"

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
silence_threshold = 1_500  # Silence threshold (RMS value)
silence_limit = 40  # Number of consecutive silent chunks before stopping
filename = "temp_output/output.wav"


def record_audio_and_transcribe() -> str:
    p = pyaudio.PyAudio()

    print("Recording...")

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(chunk)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(np.square(audio_data)))  # Calculate RMS value
        if rms < silence_threshold:
            silent_chunks += 1
            if silent_chunks >= silence_limit:
                break
        else:
            silent_chunks = 0

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b"".join(frames))


    return transcribe_audio(filename)