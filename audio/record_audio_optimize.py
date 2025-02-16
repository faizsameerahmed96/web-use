import pvporcupine
import pyaudio
import wave
import numpy as np
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key='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')

# Audio recording parameters
chunk = 512
sample_format = pyaudio.paInt16
channels = 1
fs = 16000  # Updated to match Porcupine's required sample rate
filename = "temp_output/output.wav"

# Initialize Porcupine
porcupine = pvporcupine.create(
    access_key='s78ZNl6R92RJOqDii3JTXRUWD2ooM+zV3rAC2vn+1zhymK67tV6QhA==',
    keywords=['picovoice', 'bumblebee']
)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format=sample_format,
    channels=channels,
    rate=fs,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def transcribe_audio(path: str) -> str:
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    return transcript.text

def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data)))

def record_audio():
    print("Recording...")

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(chunk)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms = calculate_rms(audio_data)
        print(rms)
        print(silence_threshold)
        if rms < silence_threshold:
            silent_chunks += 1
            if silent_chunks >= silence_limit:
                break
        else:
            silent_chunks = 0

    print("Finished recording")

    # Save the recorded data as a WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b"".join(frames))

    return filename

def record_audio_and_transcribe() -> str:
    p2 = pyaudio.PyAudio()

    print("Recording...")

    stream2 = p2.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )

    frames = []
    silent_chunks = 0

    while True:
        data = stream2.read(chunk)
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
    stream2.stop_stream()
    stream2.close()
    p2.terminate()

    print("Finished recording")

    # Save the recorded data as a WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b"".join(frames))


    print(transcribe_audio(filename))


print("Listening for wake word...")
while True:
    pcm = stream.read(porcupine.frame_length)
    audio_data = np.frombuffer(pcm, dtype=np.int16)

    # Process audio frame
    keyword_index = porcupine.process(audio_data)
    if keyword_index >= 0:
        print("Wake word detected!")
        # Analyze background noise
        background_rms = calculate_rms(audio_data)
        silence_threshold = background_rms * 1.25  # Adjust multiplier as needed
        silence_limit = int(fs / chunk * 1.25)  # 0.5 seconds of silence

        # Record audio after wake word detection
        audio_path = record_audio()
        transcription = transcribe_audio(audio_path)
        print("Transcription:", transcription)
        break
stream.stop_stream()
stream.close()
p.terminate()
porcupine.delete()



