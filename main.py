from my_browser_use import agent
import asyncio
from dotenv import load_dotenv
from audio.record_audio import record_audio_and_transcribe

load_dotenv('.env')

# asyncio.run(agent.main())

print(record_audio_and_transcribe())