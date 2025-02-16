import pyaudio
import numpy as np
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Sample rate (44.1 kHz)
silence_threshold = 500  # Silence threshold (RMS value)
silence_limit = 100  # Number of consecutive silent chunks before stopping
filename = "temp_output/record_till_pause_op.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording...')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
silent_chunks = 0  # Counter for consecutive silent chunks

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

print('Finished recording')

# Save the recorded data as a WAV file
with wave.open(filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))

print(f'Audio saved as {filename}')
