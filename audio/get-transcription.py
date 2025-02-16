import openai

# Path to your .wav file
audio_path = "../record-audio/temp_output/output.wav"


def transcribe_audio(path: str) -> str:
    with open(path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            file_name="output.wav",
            mime_type="audio/wav",
        )

    # Extract the transcribed text
    transcribed_text = response["text"]

    return transcribed_text
