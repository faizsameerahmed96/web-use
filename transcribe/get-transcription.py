import openai

# Path to your .wav file
audio_path = "../record-audio/temp_output/record_till_pause_op.wav"

# Open the audio file
with open(audio_path, "rb") as audio_file:
    # Send the audio file to OpenAI's Whisper model for transcription
    response = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        file_name="output.wav",
        mime_type="audio/wav"
    )

# Extract the transcribed text
transcribed_text = response['text']

# Define the path for the output text file
output_path = "temp_output/recorded_transcription_op.txt"

# Open the text file in write mode and save the transcription
with open(output_path, "w") as text_file:
    text_file.write(transcribed_text)

print(f"Transcription saved to {output_path}")
