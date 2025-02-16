import pyaudio
import wave
import audioop
import time

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
silence_threshold = 500  # RMS threshold for silence detection
silence_duration = 3  # Duration in seconds to detect silence
filename = "temp_output/output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
silent_chunks = 0  # Counter for consecutive silent chunks

start_time = time.time()

while True:
    data = stream.read(chunk)
    frames.append(data)
    rms = audioop.rms(data, 2)  # Calculate RMS of the chunk

    if rms < silence_threshold:
        silent_chunks += 1
    else:
        silent_chunks = 0

    # Check if silence has lasted for the specified duration
    if silent_chunks * (chunk / fs) >= silence_duration:
        break

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
with wave.open(filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
