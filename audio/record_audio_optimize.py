import wave

import numpy as np
import openai
import pvporcupine
import pyaudio

# Initialize OpenAI client
client = openai.OpenAI(
    api_key="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"
)

# Audio recording parameters
chunk = 512
sample_format = pyaudio.paInt16
channels = 1
fs = 16000  # Updated to match Porcupine's required sample rate
filename = "temp_output/output.wav"


def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data)))


porcupine = pvporcupine.create(
    access_key="saK0O0BZWvHmt3EhviUqzQloOWLaw6Leyp06CbRxUM1JdFfnCQtoPA==",
    keywords=["bumblebee"],
)


def wait_for_wakeword() -> str:
    print("Listening for wake word...")
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

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

            stream.stop_stream()
            stream.close()
            p.terminate()
            # porcupine.delete()

            return silence_threshold, silence_limit

            # Record audio after wake word detection
            # audio_path = record_audio(silence_threshold, silence_limit)
            # transcription = transcribe_audio(audio_path)
            # return transcription
            # break
