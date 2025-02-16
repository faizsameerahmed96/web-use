from dotenv import load_dotenv
load_dotenv('./.env')
from my_browser_use import agent
import asyncio

asyncio.run(agent.main())

# print(record_audio_and_transcribe())