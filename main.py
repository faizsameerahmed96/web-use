from my_browser_use import agent
import asyncio
from dotenv import load_dotenv
load_dotenv('.env')

asyncio.run(agent.main())