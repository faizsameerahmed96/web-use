from langchain_openai import ChatOpenAI
from browser_use import Agent

async def main():
    agent = Agent(
        task="Open facebook and login with faiz.ahmed@sjsu.edu and password 123456",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)