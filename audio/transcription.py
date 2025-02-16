import openai

client = openai.OpenAI()


def transcribe_audio(path: str) -> str:
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )

    transcribed_text = transcript.text

    return transcribed_text
