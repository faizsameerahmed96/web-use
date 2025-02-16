from langchain.document_loaders import AudioFileLoader

# Path to your .wav file
audio_path = "../record-audio/temp_output/output.wav"

# Initialize the audio file loader
loader = AudioFileLoader(audio_path)

# Load and transcribe the audio
documents = loader.load()

# Extract the transcribed text
transcribed_text = documents[0].page_content

print("Transcription:", transcribed_text)
