from dotenv import load_dotenv
load_dotenv('./.env')
from my_browser_use import agent
import asyncio

from langchain_openai import ChatOpenAI
asyncio.run(agent.main())

# groq_model = ChatOpenAI(model="llama-3.2-90b-vision-preview", temperature=0.2, base_url='https://api.groq.com/openai/v1/', api_key='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')

# print(groq_model.invoke("What is the capital of France?"))