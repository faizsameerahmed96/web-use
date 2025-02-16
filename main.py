from my_browser_use import agent
import asyncio
from dotenv import load_dotenv
load_dotenv('./.env')
from audio.record_audio import record_audio_and_transcribe

# asyncio.run(agent.main())

print(record_audio_and_transcribe())